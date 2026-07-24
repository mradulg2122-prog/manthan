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
    """Find the highest numeric sequence number already used in the database for the current year."""
    year = datetime.now().strftime("%Y")
    prefix_year = f"{PREFIX}{year}"

    rows = (
        db.query(Participant.registration_id)
        .filter(Participant.registration_id.like(f"{prefix_year}%"))
        .all()
    )

    max_seq = 0
    for (reg_id,) in rows:
        if reg_id and reg_id.startswith(prefix_year):
            try:
                seq = int(reg_id[len(prefix_year):])
                if seq > max_seq:
                    max_seq = seq
            except ValueError:
                pass
    return max_seq


def generate_registration_id(db: Session) -> str:
    """Generate the next unique, collision-free registration ID."""
    year = datetime.now().strftime("%Y")
    prefix_year = f"{PREFIX}{year}"
    next_num = _get_last_sequence(db) + 1

    # Safety check: guarantee candidate doesn't collide with existing database records
    while True:
        candidate = f"{prefix_year}{next_num:04d}"
        exists = (
            db.query(Participant.id)
            .filter(Participant.registration_id == candidate)
            .first()
        )
        if not exists:
            return candidate
        next_num += 1
