"""EventFlow AI - Project Configuration"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ── Project Paths ──────────────────────────────────────────────
ROOT_DIR = Path(__file__).parent
AGENTS_DIR = ROOT_DIR / "agents"
SERVICES_DIR = ROOT_DIR / "services"
ORCHESTRATOR_DIR = ROOT_DIR / "orchestrator"
DATA_DIR = ROOT_DIR / "data"

# ── Generated Output ──────────────────────────────────────────
GENERATED_DIR = ROOT_DIR / "generated"
QR_OUTPUT_DIR = GENERATED_DIR / "qr"

# ── Logs ──────────────────────────────────────────────────────
LOGS_DIR = ROOT_DIR / "logs"

# ── Credentials ──────────────────────────────────────────────
CREDENTIALS_DIR = ROOT_DIR / "credentials"
GOOGLE_OAUTH_CREDENTIALS = os.getenv(
    "GOOGLE_OAUTH_CREDENTIALS",
    str(CREDENTIALS_DIR / "credentials.json"),
)
GOOGLE_TOKEN_FILE = os.getenv(
    "GOOGLE_TOKEN_FILE",
    str(CREDENTIALS_DIR / "token.json"),
)

# ── Google Sheets ─────────────────────────────────────────────
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID", "")
GOOGLE_SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

# ── Event Info ────────────────────────────────────────────────
EVENT_NAME = os.getenv("EVENT_NAME", "EventFlow AI Conference")
ORGANIZER_NAME = os.getenv("ORGANIZER_NAME", "")
