"""Google Sheet Service - Handles authentication and data retrieval."""

import os
import gspread
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from config import GOOGLE_OAUTH_CREDENTIALS, GOOGLE_TOKEN_FILE, GOOGLE_SHEET_ID, GOOGLE_SCOPES


class GoogleSheetService:
    """Connects to Google Sheets and reads data."""

    def __init__(self):
        self.client = None
        self.spreadsheet = None
        self.worksheet = None

    def authenticate(self):
        """Authenticate using OAuth Desktop flow (credentials.json + token.json)."""
        if not os.path.exists(GOOGLE_OAUTH_CREDENTIALS):
            raise FileNotFoundError(
                f"OAuth credentials not found: {GOOGLE_OAUTH_CREDENTIALS}\n"
                "Download credentials.json from Google Cloud Console → APIs & Services → Credentials\n"
                "and place it in the credentials/ folder."
            )

        creds = None

        # Load cached token if it exists
        if os.path.exists(GOOGLE_TOKEN_FILE):
            try:
                creds = Credentials.from_authorized_user_file(GOOGLE_TOKEN_FILE, GOOGLE_SCOPES)
            except Exception:
                creds = None

        # Refresh or run new OAuth flow
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception:
                    creds = None

            if not creds:
                try:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        GOOGLE_OAUTH_CREDENTIALS, GOOGLE_SCOPES
                    )
                    creds = flow.run_local_server(port=0)
                except Exception as e:
                    raise ConnectionError(f"OAuth authentication failed: {e}")

            # Save token for next run
            with open(GOOGLE_TOKEN_FILE, "w") as token_file:
                token_file.write(creds.to_json())

        try:
            self.client = gspread.authorize(creds)
        except Exception as e:
            raise ConnectionError(f"Google Sheets authorization failed: {e}")

    def connect_to_sheet(self, sheet_id=None):
        """Open the Google Sheet by ID."""
        target_id = sheet_id or GOOGLE_SHEET_ID

        if not target_id:
            raise ValueError(
                "GOOGLE_SHEET_ID is not set. Update your .env file."
            )

        if not self.client:
            self.authenticate()

        try:
            self.spreadsheet = self.client.open_by_key(target_id)
        except gspread.SpreadsheetNotFound:
            raise FileNotFoundError(
                f"Sheet not found: {target_id}\n"
                "Check the GOOGLE_SHEET_ID and share the sheet with the service account."
            )
        except Exception as e:
            raise ConnectionError(f"Failed to open sheet: {e}")

    def open_worksheet(self, worksheet_name="Sheet1"):
        """Open a specific worksheet by name."""
        if not self.spreadsheet:
            raise ConnectionError("Not connected to any sheet. Call connect_to_sheet() first.")

        try:
            self.worksheet = self.spreadsheet.worksheet(worksheet_name)
        except gspread.WorksheetNotFound:
            raise FileNotFoundError(
                f"Worksheet '{worksheet_name}' not found.\n"
                f"Available: {[ws.title for ws in self.spreadsheet.worksheets()]}"
            )

    def get_all_rows(self, worksheet_name="Sheet1"):
        """Read all rows and return as a list of dictionaries."""
        if not self.spreadsheet:
            self.connect_to_sheet()

        self.open_worksheet(worksheet_name)
        rows = self.worksheet.get_all_records()
        return rows

