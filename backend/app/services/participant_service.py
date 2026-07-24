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


def create_participant(db: Session, data: ParticipantCreate) -> Participant:
    """Insert a new participant row and return it."""
    participant = Participant(
        name=data.name,
        email=data.email,
        phone=data.phone,
        college=data.college,
        event=data.event,
        attendance_status="Absent",
        qr_sent=False,
        email_sent=False,
    )
    db.add(participant)
    db.commit()
    db.refresh(participant)
    return participant
