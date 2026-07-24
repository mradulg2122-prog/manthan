"""
User model.
Stores admin and volunteer accounts.
"""

from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, DateTime

from app.database.database import Base


class User(Base):
    """An admin or volunteer user."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)  # bcrypt hash
    role = Column(String, nullable=False)       # ADMIN or VOLUNTEER
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<User {self.email} ({self.role})>"
