from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from app.database.database import get_db, SessionLocal
from app.schemas.participant import ParticipantCreate, ParticipantResponse
from app.models.participant import Participant
from app.services.participant_service import (
    is_email_taken,
    is_phone_duplicate_for_event,
    get_registration_count,
    create_participant,
)
from app.services.email_service import send_qr_email
from app.services.google_sheets_service import append_participant as sheets_append

logger = logging.getLogger("eventflow.registration")

MAX_REGISTRATIONS = 100

router = APIRouter(tags=["Registration"])


def _dispatch_email_task(pid: int, email: str, name: str, reg_id: str, qr_path: str, event: str) -> None:
    """Guaranteed background task executed by FastAPI after returning 201 response."""
    logger.info("🚀 [BackgroundTasks] Starting immediate email dispatch for %s (%s)...", name, email)
    email_success = False
    try:
        send_qr_email(
            recipient_email=email,
            recipient_name=name,
            registration_id=reg_id,
            qr_image_path=qr_path,
            event_name=event,
        )
        email_success = True
        logger.info("✅ [BackgroundTasks] Email successfully sent to %s (%s)", name, email)
    except Exception as e:
        logger.error("❌ [BackgroundTasks] Email dispatch failed for %s: %s", email, e)

    # Update database
    db = SessionLocal()
    try:
        p = db.query(Participant).filter(Participant.id == pid).first()
        if p:
            if email_success:
                p.email_sent = True
            p.qr_sent = True
            db.commit()
            db.refresh(p)
            try:
                sheets_append(p)
            except Exception:
                pass
    except Exception as e:
        logger.error("Error updating participant in background task: %s", e)
    finally:
        db.close()


@router.post("/register", response_model=ParticipantResponse, status_code=201)
def register_participant(
    data: ParticipantCreate,
    background_tasks: BackgroundTasks,
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
            detail={"success": False, "message": "Participant already registered with this email."},
        )

    # --- Duplicate phone + same event check ---
    if is_phone_duplicate_for_event(db, data.phone, data.event):
        raise HTTPException(
            status_code=409,
            detail={"success": False, "message": "Participant already registered with this phone number."},
        )

    # --- Save to database with Instant ID & QR ---
    participant, reg_id, qr_path = create_participant(db, data)
    pid = participant.id
    logger.info("✓ Saved participant %d (%s) with Registration ID %s", pid, participant.name, reg_id)

    # Enqueue guaranteed background task via FastAPI
    background_tasks.add_task(
        _dispatch_email_task,
        pid,
        data.email,
        data.name,
        reg_id,
        qr_path,
        data.event,
    )

    return ParticipantResponse(
        success=True,
        message="Registration successful.",
        participant_id=pid,
    )



