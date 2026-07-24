"""
Pydantic schemas for participant registration.
Handles request validation and response formatting.
"""

import re
from pydantic import BaseModel, EmailStr, field_validator


class ParticipantCreate(BaseModel):
    """Request body for POST /register."""

    name: str
    email: EmailStr
    phone: str
    college: str
    event: str

    # --- Strip whitespace from all string fields ---

    @field_validator("name", "phone", "college", "event", mode="before")
    @classmethod
    def strip_whitespace(cls, value: str) -> str:
        if isinstance(value, str):
            return value.strip()
        return value

    # --- Phone must be exactly 10 digits ---

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: str) -> str:
        digits = re.sub(r"\D", "", value)  # keep only digits
        if len(digits) != 10:
            raise ValueError("Phone must contain exactly 10 digits.")
        return digits


class ParticipantResponse(BaseModel):
    """Response body for a successful registration."""

    success: bool
    message: str
    participant_id: int
