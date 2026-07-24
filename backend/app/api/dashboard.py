"""
Dashboard API router.
Admin-only endpoints for stats, participants, attendance, activity, and export.
"""

import io
import logging
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.database.database import get_db
from app.models.participant import Participant
from app.services.auth_service import require_admin

logger = logging.getLogger("eventflow.dashboard")

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


# ─── Stats ────────────────────────────────────────────────────────────────────
@router.get("/stats")
def get_stats(db: Session = Depends(get_db), _=Depends(require_admin)):
    """Return registration and attendance statistics."""
    total = db.query(Participant).count()
    present = db.query(Participant).filter(Participant.attendance_status == "Present").count()
    absent = total - present
    percentage = round((present / total) * 100, 1) if total > 0 else 0

    return {
        "total": total,
        "present": present,
        "absent": absent,
        "percentage": percentage,
    }


# ─── Participants list ────────────────────────────────────────────────────────
@router.get("/participants")
def get_participants(
    search: str = Query("", description="Search by name, email, or registration ID"),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    sort_by: str = Query("id", description="Column to sort by"),
    sort_order: str = Query("desc", description="asc or desc"),
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    """Return a paginated list of participants."""
    query = db.query(Participant)

    # Search
    if search:
        pattern = f"%{search}%"
        query = query.filter(
            Participant.name.ilike(pattern)
            | Participant.email.ilike(pattern)
            | Participant.registration_id.ilike(pattern)
        )

    # Sort
    sort_column = getattr(Participant, sort_by, Participant.id)
    if sort_order == "asc":
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())

    # Count
    total = query.count()

    # Paginate
    participants = query.offset((page - 1) * per_page).limit(per_page).all()

    rows = []
    for p in participants:
        rows.append({
            "id": p.id,
            "registration_id": p.registration_id or "",
            "name": p.name,
            "email": p.email,
            "phone": p.phone or "",
            "attendance_status": p.attendance_status or "Absent",
            "check_in_time": p.check_in_time.strftime("%I:%M %p") if p.check_in_time else "",
        })

    return {
        "participants": rows,
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": max(1, -(-total // per_page)),  # ceil division
    }


# ─── Single participant detail ───────────────────────────────────────────────
@router.get("/participant/{registration_id}")
def get_participant_detail(
    registration_id: str,
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    """Return full details for a single participant."""
    p = db.query(Participant).filter(Participant.registration_id == registration_id).first()

    if not p:
        return {"error": "Participant not found."}

    return {
        "registration_id": p.registration_id or "",
        "name": p.name,
        "email": p.email,
        "phone": p.phone or "",
        "college": p.college or "",
        "event": p.event or "",
        "attendance_status": p.attendance_status or "Absent",
        "check_in_time": p.check_in_time.strftime("%I:%M %p") if p.check_in_time else "",
        "qr_sent": p.qr_sent,
        "email_sent": p.email_sent,
    }


# ─── Manual attendance toggle ────────────────────────────────────────────────
@router.patch("/participant/{registration_id}/attendance")
def update_attendance(
    registration_id: str,
    action: str = Query(..., description="present or absent"),
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    """Mark a participant as Present or Absent manually."""
    p = db.query(Participant).filter(Participant.registration_id == registration_id).first()

    if not p:
        return {"error": "Participant not found."}

    if action == "present":
        p.attendance_status = "Present"
        p.check_in_time = datetime.now(timezone.utc)
    else:
        p.attendance_status = "Absent"
        p.check_in_time = None

    db.commit()
    logger.info("Manual attendance: %s → %s", registration_id, action)

    return {
        "success": True,
        "registration_id": registration_id,
        "attendance_status": p.attendance_status,
        "check_in_time": p.check_in_time.strftime("%I:%M %p") if p.check_in_time else "",
    }


# ─── Activity feed ───────────────────────────────────────────────────────────
@router.get("/activity")
def get_activity(
    limit: int = Query(20, ge=1, le=50),
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    """Return the latest check-in activity (newest first)."""
    rows = (
        db.query(Participant)
        .filter(Participant.check_in_time.isnot(None))
        .order_by(desc(Participant.check_in_time))
        .limit(limit)
        .all()
    )

    return [
        {
            "name": r.name,
            "registration_id": r.registration_id or "",
            "time": r.check_in_time.strftime("%I:%M %p") if r.check_in_time else "",
            "status": r.attendance_status,
        }
        for r in rows
    ]


# ─── Export Excel ─────────────────────────────────────────────────────────────
@router.get("/export")
def export_attendance(
    token: str = Query(..., description="JWT token"),
    db: Session = Depends(get_db),
):
    """Export all participants as an Excel file. Token passed as query param for browser downloads."""
    from app.services.auth_service import decode_token as _decode
    payload = _decode(token)
    if not payload or payload.get("role") != "ADMIN":
        from fastapi import HTTPException, status
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required.")

    import openpyxl

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Attendance"

    # Header
    headers = ["Registration ID", "Name", "Email", "Phone", "Attendance", "Check-in Time"]
    ws.append(headers)

    # Data
    participants = db.query(Participant).order_by(Participant.id).all()
    for p in participants:
        ws.append([
            p.registration_id or "",
            p.name,
            p.email,
            p.phone or "",
            p.attendance_status or "Absent",
            p.check_in_time.strftime("%Y-%m-%d %I:%M %p") if p.check_in_time else "",
        ])

    # Stream the file
    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)

    filename = f"Youth_Parliament_6.0_Attendance_{datetime.now().strftime('%Y-%m-%d')}.xlsx"
    return StreamingResponse(
        buffer,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )
