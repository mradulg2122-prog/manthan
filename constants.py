"""EventFlow AI - Project Constants"""

# ── Sheet Column Names (must match Google Sheet headers) ─────
COL_REGISTRATION_ID = "registration_id"
COL_NAME = "What is Your name"
COL_EMAIL = "email id"
COL_PHONE = "phone"
COL_EVENT = "event"
COL_ATTENDANCE_STATUS = "Attendance Status"
COL_CHECK_IN_TIME = "CheckIn_Time"

# ── Worksheet Name ────────────────────────────────────────────
WORKSHEET_NAME = "Form Responses 1"

# ── Attendance Status Values ──────────────────────────────────
STATUS_REGISTERED = "Registered"
STATUS_CHECKED_IN = "Present"
STATUS_ABSENT = "Absent"

# ── Registration ID Prefix ────────────────────────────────────
REGISTRATION_ID_PREFIX = "EVT"

# ── QR Code Settings ─────────────────────────────────────────
QR_IMAGE_SIZE = (300, 300)  # width x height in pixels

# ── Supported File Names ─────────────────────────────────────
REGISTRATIONS_FILE = "registrations.xlsx"
ATTENDANCE_REPORT_FILE = "attendance_report.xlsx"
LOG_FILE = "eventflow.log"
