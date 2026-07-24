"""
Registration ID Service.
Generates unique IDs like EVT20260001, EVT20260002, etc.
"""

from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.models.participant import Participant

PREFIX = "EVT"


def _get_last_sequence(db: Session) -> int:
    """Find the highest sequence number already used in the database."""
    year = datetime.now().strftime("%Y")
    prefix_year = f"{PREFIX}{year}"

    # Get the latest registration_id that starts with our prefix
    row = (
        db.query(Participant)
        .filter(Participant.registration_id.like(f"{prefix_year}%"))
        .order_by(desc(Participant.registration_id))
        .first()
    )

    if row and row.registration_id:
        try:
            return int(row.registration_id[len(prefix_year):])
        except ValueError:
            return 0
    return 0


def generate_registration_id(db: Session) -> str:
    """Generate the next unique registration ID."""
    year = datetime.now().strftime("%Y")
    next_num = _get_last_sequence(db) + 1
    return f"{PREFIX}{year}{next_num:04d}"
