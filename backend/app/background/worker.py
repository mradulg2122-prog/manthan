"""
Worker.
Processes one participant at a time through the pipeline:
  Registration ID → QR Code → Email → Update DB
Only one worker runs at a time (lock-based).
"""

import os
import logging
import threading

from app.database.database import SessionLocal
from app.models.participant import Participant
from app.services.registration_id_service import generate_registration_id
from app.services.qr_service import generate_and_save_qr
from app.services.email_service import send_qr_email
from app.background import queue_manager

logger = logging.getLogger("eventflow.worker")

# ---------------------------------------------------------------------------
# Worker lock — only one worker thread processes the queue at a time
# ---------------------------------------------------------------------------
_worker_lock = threading.Lock()


# ---------------------------------------------------------------------------
# Pipeline — runs for a single participant
# ---------------------------------------------------------------------------
def _process_one(participant_id: int) -> None:
    """Run the full pipeline for one participant with skip + retry logic."""
    db = SessionLocal()
    try:
        participant = db.query(Participant).filter(Participant.id == participant_id).first()

        if not participant:
            logger.warning("Participant %d not found — skipping.", participant_id)
            return

        # Skip if fully processed already
        if participant.registration_id and participant.qr_sent and participant.email_sent:
            logger.info("Participant %d already fully processed — skipping.", participant_id)
            return

        logger.info("Processing Participant: %s (id=%d)", participant.name, participant.id)

        # ------------------------------------------------------------------
        # Step 1 — Registration ID (skip if already assigned)
        # ------------------------------------------------------------------
        reg_id = participant.registration_id
        if not reg_id:
            reg_id = generate_registration_id(db)
            participant.registration_id = reg_id
            db.commit()
            logger.info("  Registration ID Generated: %s", reg_id)
        else:
            logger.info("  Registration ID exists: %s — skipping.", reg_id)

        # ------------------------------------------------------------------
        # Step 2 — QR Code (regenerate if qr_sent is False OR file missing on disk)
        # ------------------------------------------------------------------
        qr_path = os.path.join("generated", "qr", f"{reg_id}.png")
        if not participant.qr_sent or not os.path.exists(qr_path):
            try:
                qr_path = generate_and_save_qr(reg_id)
                participant.qr_sent = True
                db.commit()
                logger.info("  ✓ QR Generated/Verified on disk: %s", qr_path)
            except Exception as e:
                db.rollback()
                logger.error("  ✗ QR generation FAILED: %s — skipping email.", e)
                return  # Don't send email if QR failed
        else:
            logger.info("  ✓ QR already exists on disk: %s — skipping QR generation.", qr_path)

        # ------------------------------------------------------------------
        # Step 3 — Email (skip if email_sent is already True)
        # ------------------------------------------------------------------
        if not participant.email_sent:
            try:
                event_name = participant.event or "EventFlow Pro"
                send_qr_email(
                    recipient_email=participant.email,
                    recipient_name=participant.name,
                    registration_id=reg_id,
                    qr_image_path=qr_path,
                    event_name=event_name,
                )
                participant.email_sent = True
                db.commit()
                logger.info("  ✓ Email Sent to: %s", participant.email)
            except Exception as e:
                db.rollback()
                # Keep email_sent = False so watcher can retry next cycle
                logger.error("  ✗ Email FAILED for %s: %s — will retry next cycle.", participant.email, e)
                return
        else:
            logger.info("  ✓ Email already sent — skipping.")

        # ------------------------------------------------------------------
        # Step 4 — Log completion
        # ------------------------------------------------------------------
        logger.info("  ✓ Database Updated (registration_id=%s, qr_sent=True, email_sent=True).", reg_id)
        logger.info("  ✓ Completed processing for participant ID %d (%s)", participant.id, reg_id)

    except Exception as e:
        db.rollback()
        logger.error("  FAILED for participant %d: %s — skipping.", participant_id, e)
    finally:
        db.close()
        # Clear from in-flight set so watcher can re-enqueue on failure
        try:
            from app.background.watcher import clear_in_flight
            clear_in_flight(participant_id)
        except Exception:
            pass


# ---------------------------------------------------------------------------
# Drain the queue — called by the watcher after enqueuing new participants
# ---------------------------------------------------------------------------
def process_queue() -> None:
    """
    Drain the queue one item at a time.
    Uses a lock so only one thread can run this at a time.
    If the lock is already held, the call returns immediately
    (the existing worker will pick up any new items).
    """
    acquired = _worker_lock.acquire(blocking=False)
    if not acquired:
        # Another worker is already running — it will drain new items too
        return

    try:
        while not queue_manager.is_empty():
            participant_id = queue_manager.dequeue()
            if participant_id is not None:
                _process_one(participant_id)
    finally:
        _worker_lock.release()
