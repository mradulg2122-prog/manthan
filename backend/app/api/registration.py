"""
Registration API router.
Handles POST /register for new participant sign-ups.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.participant import ParticipantCreate, ParticipantResponse
from app.services.participant_service import (
    is_email_taken,
    is_phone_duplicate_for_event,
    create_participant,
)

router = APIRouter(tags=["Registration"])


@router.post("/register", response_model=ParticipantResponse, status_code=201)
def register_participant(
    data: ParticipantCreate,
    db: Session = Depends(get_db),
):
    """Register a new participant for an event."""

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

    # --- Save to database ---
    participant = create_participant(db, data)

    return ParticipantResponse(
        success=True,
        message="Registration successful.",
        participant_id=participant.id,
    )
