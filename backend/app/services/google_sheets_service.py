"""
Google Sheets backup service.
Appends participant data to a Google Sheet on registration and
updates attendance on QR scan.  Uses Google Service Account auth.

This is a SECONDARY backup — failures here never block the primary
PostgreSQL pipeline.
"""

import json
import logging
import os
import threading
from datetime import datetime

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

logger = logging.getLogger("eventflow.sheets")

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# Expected column order (row 1 header)
HEADERS = [
    "Registration ID",
    "Name",
    "Email",
    "Phone",
    "College",
    "Event",
    "Registration Time",
    "Attendance Status",
    "Check-in Time",
    "QR Sent",
    "Email Sent",
]

# ---------------------------------------------------------------------------
# Singleton service client (thread-safe lazy init)
# ---------------------------------------------------------------------------
_service = None
_lock = threading.Lock()


def _get_credentials():
    """Build service-account credentials from env."""
    # Option 1: JSON string in GOOGLE_SERVICE_ACCOUNT_JSON
    json_str = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON", "")
    if json_str:
        info = json.loads(json_str)
        return service_account.Credentials.from_service_account_info(info, scopes=SCOPES)

    # Option 2: File path in GOOGLE_SERVICE_ACCOUNT_FILE
    file_path = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE", "")
    if file_path and os.path.isfile(file_path):
        return service_account.Credentials.from_service_account_file(file_path, scopes=SCOPES)

    return None


def _get_service():
    """Return a cached Sheets API service (or None if not configured)."""
    global _service
    if _service is not None:
        return _service

    with _lock:
        if _service is not None:  # Double-check
            return _service

        creds = _get_credentials()
        if creds is None:
            logger.warning(
                "Google Sheets not configured — set GOOGLE_SERVICE_ACCOUNT_JSON "
                "or GOOGLE_SERVICE_ACCOUNT_FILE env variable."
            )
            return None

        _service = build("sheets", "v4", credentials=creds, cache_discovery=False)
        logger.info("Google Sheets API client initialised.")
        return _service


def _get_sheet_id() -> str | None:
    """Return the spreadsheet ID from env, or None."""
    sheet_id = os.getenv("GOOGLE_SHEET_ID", "")
    return sheet_id if sheet_id else None


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------
def _ensure_headers(service, spreadsheet_id: str, sheet_name: str = "Sheet1"):
    """Create header row if the sheet is empty."""
    result = (
        service.spreadsheets()
        .values()
        .get(spreadsheetId=spreadsheet_id, range=f"{sheet_name}!A1:K1")
        .execute()
    )
    values = result.get("values", [])
    if not values:
        service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=f"{sheet_name}!A1:K1",
            valueInputOption="RAW",
            body={"values": [HEADERS]},
        ).execute()
        logger.info("Google Sheet headers created.")


def _find_row_by_reg_id(service, spreadsheet_id: str, registration_id: str, sheet_name: str = "Sheet1") -> int | None:
    """Find the row number for a given Registration ID. Returns 1-based row index or None."""
    result = (
        service.spreadsheets()
        .values()
        .get(spreadsheetId=spreadsheet_id, range=f"{sheet_name}!A:A")
        .execute()
    )
    values = result.get("values", [])
    for i, row in enumerate(values):
        if row and row[0] == registration_id:
            return i + 1  # 1-based
    return None


def _fmt_datetime(dt) -> str:
    """Format a datetime for the sheet, or return empty string."""
    if dt is None:
        return ""
    if isinstance(dt, datetime):
        return dt.strftime("%Y-%m-%d %H:%M:%S UTC")
    return str(dt)


def _bool_str(val) -> str:
    return "Yes" if val else "No"


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
def append_participant(participant) -> bool:
    """
    Append (or update if already exists) a participant row after registration.
    Returns True on success, False on failure.
    Never raises — logs errors instead.
    """
    try:
        service = _get_service()
        sheet_id = _get_sheet_id()
        if not service or not sheet_id:
            return False

        _ensure_headers(service, sheet_id)

        reg_id = participant.registration_id or ""

        row_data = [
            reg_id,
            participant.name or "",
            participant.email or "",
            participant.phone or "",
            participant.college or "",
            participant.event or "",
            _fmt_datetime(participant.created_at),
            participant.attendance_status or "Absent",
            _fmt_datetime(participant.check_in_time),
            _bool_str(participant.qr_sent),
            _bool_str(participant.email_sent),
        ]

        # Check if row already exists (avoid duplicates)
        if reg_id:
            existing_row = _find_row_by_reg_id(service, sheet_id, reg_id)
            if existing_row:
                # Update existing row
                service.spreadsheets().values().update(
                    spreadsheetId=sheet_id,
                    range=f"Sheet1!A{existing_row}:K{existing_row}",
                    valueInputOption="RAW",
                    body={"values": [row_data]},
                ).execute()
                logger.info("Google Sheet: Updated existing row %d for %s", existing_row, reg_id)
                return True

        # Append new row
        service.spreadsheets().values().append(
            spreadsheetId=sheet_id,
            range="Sheet1!A:K",
            valueInputOption="RAW",
            insertDataOption="INSERT_ROWS",
            body={"values": [row_data]},
        ).execute()
        logger.info("Google Sheet: Appended row for %s", reg_id)
        return True

    except HttpError as e:
        logger.error("Google Sheet append FAILED (HTTP %s): %s", e.resp.status, e)
        return False
    except Exception as e:
        logger.error("Google Sheet append FAILED: %s", e)
        return False


def update_attendance(registration_id: str, status: str = "Present", check_in_time=None) -> bool:
    """
    Update Attendance Status and Check-in Time for a participant row.
    Returns True on success, False on failure.
    Never raises — logs errors instead.
    """
    try:
        service = _get_service()
        sheet_id = _get_sheet_id()
        if not service or not sheet_id:
            return False

        row_num = _find_row_by_reg_id(service, sheet_id, registration_id)
        if not row_num:
            logger.warning("Google Sheet: Row not found for %s — cannot update attendance.", registration_id)
            return False

        # Update columns H (Attendance Status) and I (Check-in Time) — columns 8 and 9
        service.spreadsheets().values().update(
            spreadsheetId=sheet_id,
            range=f"Sheet1!H{row_num}:I{row_num}",
            valueInputOption="RAW",
            body={"values": [[status, _fmt_datetime(check_in_time)]]},
        ).execute()
        logger.info("Google Sheet: Attendance updated for %s → %s", registration_id, status)
        return True

    except HttpError as e:
        logger.error("Google Sheet attendance update FAILED (HTTP %s): %s", e.resp.status, e)
        return False
    except Exception as e:
        logger.error("Google Sheet attendance update FAILED: %s", e)
        return False
