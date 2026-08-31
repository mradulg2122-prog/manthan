"""
Registration API router.
Handles POST /register for new participant sign-ups.
"""

import logging
import threading

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.participant import ParticipantCreate, ParticipantResponse
from app.services.participant_service import (
    is_email_taken,
    is_phone_duplicate_for_event,
    get_registration_count,
    create_participant,
)
from app.background.worker import _process_one

logger = logging.getLogger("eventflow.registration")

MAX_REGISTRATIONS = 100

router = APIRouter(tags=["Registration"])


@router.post("/register", response_model=ParticipantResponse, status_code=201)
def register_participant(
    data: ParticipantCreate,
    db: Session = Depends(get_db),
):
    """Register a new participant for an event."""

    # --- Max 100 registrations cap ---
    current_count = get_registration_count(db)
    if current_count >= MAX_REGISTRATIONS:
        raise HTTPException(
            status_code=400,
            detail={
                "success": False,
                "message": f"Registrations for MANTHAN have reached the maximum limit of {MAX_REGISTRATIONS} participants. Registrations are now closed.",
            },
        )

    # --- Duplicate email check ---
    if is_email_taken(db, data.email):
        raise HTTPException(
            status_code=409,
            detail={"success": False, "message": "Participant already registered."},
        )

    # --- Duplicate phone + same event check ---
    if is_phone_duplicate_for_event(db, data.phone, data.event):
        raise HTTPException(
            status_code=409,
            detail={"success": False, "message": "Participant already registered."},
        )

    # --- Save to database with Instant ID & QR ---
    participant, reg_id, qr_path = create_participant(db, data)
    pid = participant.id
    logger.info("✓ Saved participant %d (%s) with Registration ID %s", pid, participant.name, reg_id)

    # --- Instant sub-second email dispatch ---
    def _instant_email_dispatch():
        try:
            send_qr_email(
                recipient_email=data.email,
                recipient_name=data.name,
                registration_id=reg_id,
                qr_image_path=qr_path,
                event_name=data.event,
            )
            # Update DB status
            from app.database.database import SessionLocal
            db_inner = SessionLocal()
            try:
                p = db_inner.query(Participant).filter(Participant.id == pid).first()
                if p:
                    p.email_sent = True
                    db_inner.commit()
            finally:
                db_inner.close()
        except Exception as e:
            logger.error("Instant email failed for %s: %s (Watcher will retry automatically).", data.email, e)

    threading.Thread(
        target=_instant_email_dispatch,
        daemon=True,
        name=f"fast-mail-{pid}",
    ).start()

    return ParticipantResponse(
        success=True,
        message="Registration successful.",
        participant_id=pid,
    )


