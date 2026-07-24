"""
Scan API router.
Handles POST /scan for QR-based attendance check-in.
"""

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.participant import Participant
from app.schemas.scan import ScanRequest

router = APIRouter(tags=["Scanner"])


@router.post("/scan")
def scan_qr(data: ScanRequest, db: Session = Depends(get_db)):
    """Mark a participant as present by scanning their QR registration ID."""

    # Find participant
    participant = (
        db.query(Participant)
        .filter(Participant.registration_id == data.registration_id)
        .first()
    )

    if not participant:
        raise HTTPException(
            status_code=404,
            detail={"success": False, "message": "Invalid QR Code"},
        )

    # Already checked in
    if participant.attendance_status == "Present":
        return {
            "success": False,
            "message": "Participant already checked in.",
            "name": participant.name,
        }

    # Mark present
    now = datetime.now(timezone.utc)
    participant.attendance_status = "Present"
    participant.check_in_time = now
    db.commit()

    return {
        "success": True,
        "name": participant.name,
        "event": participant.event or "",
        "time": now.strftime("%I:%M %p"),
    }
