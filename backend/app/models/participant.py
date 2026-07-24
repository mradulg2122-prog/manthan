"""
Participant model.
Represents an event attendee in the database.
"""

from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, Boolean, DateTime

from app.database.database import Base


class Participant(Base):
    """A single event participant / attendee."""

    __tablename__ = "participants"

    # Primary key
    id = Column(Integer, primary_key=True, index=True)

    # Registration
    registration_id = Column(String, unique=True, nullable=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=True)
    college = Column(String, nullable=True)
    event = Column(String, nullable=True)

    # Attendance
    attendance_status = Column(String, default="Absent")
    check_in_time = Column(DateTime, nullable=True)

    # Flags
    qr_sent = Column(Boolean, default=False)
    email_sent = Column(Boolean, default=False)

    # Timestamps
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self):
        return f"<Participant {self.registration_id} — {self.name}>"
