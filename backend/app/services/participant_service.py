"""
Participant service.
Handles saving a new participant to the database.
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models.participant import Participant
from app.schemas.participant import ParticipantCreate


def is_email_taken(db: Session, email: str) -> bool:
    """Check if a participant with this email already exists."""
    return db.query(Participant).filter(Participant.email == email).first() is not None


def is_phone_duplicate_for_event(db: Session, phone: str, event: str) -> bool:
    """Check if the same phone is already registered for this event."""
    return (
        db.query(Participant)
        .filter(and_(Participant.phone == phone, Participant.event == event))
        .first()
        is not None
    )


def get_registration_count(db: Session, event: str = "MANTHAN | The Freshers' Showdown") -> int:
    """Return current count of registered participants."""
    return db.query(Participant).count()


def create_participant(db: Session, data: ParticipantCreate) -> tuple[Participant, str, str]:
    """Insert a new participant row with instant Registration ID and QR Code in 1 step."""
    from app.services.registration_id_service import generate_registration_id
    from app.services.qr_service import generate_and_save_qr

    reg_id = generate_registration_id(db)
    qr_path = generate_and_save_qr(reg_id)

    participant = Participant(
        registration_id=reg_id,
        name=data.name,
        email=data.email,
        phone=data.phone,
        college=data.college,
        event=data.event,
        attendance_status="Absent",
        qr_sent=True,
        email_sent=False,
    )
    db.add(participant)
    db.commit()
    db.refresh(participant)
    return participant, reg_id, qr_path

