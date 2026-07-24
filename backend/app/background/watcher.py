"""
Watcher.
Runs in a background thread alongside FastAPI.
Every 5 seconds it checks PostgreSQL for new participants
(registration_id IS NULL) and feeds them into the queue → worker pipeline.
"""

import logging
import threading

from app.database.database import SessionLocal
from app.models.participant import Participant
from app.background import queue_manager
from app.background.worker import process_queue

logger = logging.getLogger("eventflow.watcher")

# ---------------------------------------------------------------------------
# Watcher control
# ---------------------------------------------------------------------------
_stop_event = threading.Event()

POLL_INTERVAL = 5  # seconds

# Track participant IDs currently being processed to prevent duplicates
_in_flight: set = set()
_in_flight_lock = threading.Lock()


def mark_in_flight(pid: int) -> None:
    """Mark a participant ID as currently being processed."""
    with _in_flight_lock:
        _in_flight.add(pid)


def clear_in_flight(pid: int) -> None:
    """Remove a participant ID from the in-flight set."""
    with _in_flight_lock:
        _in_flight.discard(pid)


def is_in_flight(pid: int) -> bool:
    """Check if a participant ID is currently being processed."""
    with _in_flight_lock:
        return pid in _in_flight


def _watch_loop() -> None:
    """Main loop — polls for unprocessed participants every POLL_INTERVAL seconds."""
    logger.info("👁️  Watcher Started")

    while not _stop_event.is_set():
        try:
            db = SessionLocal()
            try:
                # Query database state: find all pending participants where email_sent is False
                new_participants = (
                    db.query(Participant.id)
                    .filter(
                        (Participant.email_sent.is_(False))
                        | (Participant.email_sent.is_(None))
                    )
                    .order_by(Participant.id)
                    .all()
                )
            finally:
                db.close()

            # Enqueue only participants not already in-flight
            enqueued = 0
            for (pid,) in new_participants:
                if not is_in_flight(pid):
                    mark_in_flight(pid)
                    queue_manager.enqueue(pid)
                    enqueued += 1

            if enqueued > 0:
                logger.info("Enqueued %d participant(s). Queue size: %d", enqueued, queue_manager.size())
                # Kick off the worker (non-blocking if already running)
                process_queue()

        except Exception as e:
            # Recover from DB disconnect, network errors, etc.
            logger.error("Watcher error: %s — retrying next cycle.", e)

        # Sleep in small increments so we can respond to stop quickly
        _stop_event.wait(timeout=POLL_INTERVAL)

    logger.info("👁️  Watcher Stopped")


# ---------------------------------------------------------------------------
# Public API — called from main.py startup/shutdown
# ---------------------------------------------------------------------------
_thread: threading.Thread | None = None


def start_watcher() -> None:
    """Start the watcher in a daemon background thread."""
    global _thread
    _stop_event.clear()
    _thread = threading.Thread(target=_watch_loop, daemon=True, name="watcher")
    _thread.start()


def stop_watcher() -> None:
    """Signal the watcher to finish its current work and exit."""
    _stop_event.set()
    if _thread is not None:
        _thread.join(timeout=10)


def watcher_is_running() -> bool:
    """Check if the watcher thread is alive."""
    return _thread is not None and _thread.is_alive()
