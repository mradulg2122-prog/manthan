"""Registration Agent - Reads and cleans participant data from Google Sheets."""

import sys
import os

# Allow running as: python agents/registration_agent.py
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.google_sheet_service import GoogleSheetService
from constants import WORKSHEET_NAME


class RegistrationAgent:
    """Reads registrations and returns clean participant data."""

    def __init__(self):
        self.sheet_service = GoogleSheetService()

    def fetch_registrations(self, worksheet_name=WORKSHEET_NAME):
        """Fetch all registrations from the sheet."""
        self.sheet_service.authenticate()
        self.sheet_service.connect_to_sheet()
        rows = self.sheet_service.get_all_rows(worksheet_name)
        return rows

    def clean_row(self, row):
        """Trim whitespace and extract required fields."""
        return {
            "name": row.get("What is Your name", "").strip(),
            "email": row.get("email id", "").strip(),
            "phone": str(row.get("phone", "")).strip(),
            "college": row.get("college", "").strip(),
            "event": row.get("event", "").strip(),
            "registration_id": row.get("registration_id", "").strip(),
            "qr_sent": row.get("qr_sent", "").strip(),
            "email_sent": row.get("email_sent", "").strip(),
            "attendance_status": row.get("Attendance Status", "").strip(),
            "check_in_time": row.get("CheckIn_Time", "").strip(),
        }

    def is_valid_row(self, row):
        """Check if the row has at least a name and email."""
        return bool(row.get("name")) and bool(row.get("email"))

    def get_clean_registrations(self, worksheet_name=WORKSHEET_NAME):
        """Fetch, clean, and filter registrations."""
        raw_rows = self.fetch_registrations(worksheet_name)
        clean_data = []

        for row in raw_rows:
            cleaned = self.clean_row(row)
            if self.is_valid_row(cleaned):
                clean_data.append(cleaned)

        return raw_rows, clean_data


def main():
    """Test the Registration Agent."""
    agent = RegistrationAgent()

    try:
        raw_rows, clean_data = agent.get_clean_registrations()
        print(f"\n✓ Connected to Google Sheet")
        print(f"✓ Total registrations: {len(raw_rows)}")
        print(f"✓ Valid registrations: {len(clean_data)}")

        # Preview first 3 entries
        if clean_data:
            print(f"\n--- Preview (first 3) ---")
            for entry in clean_data[:3]:
                print(f"  {entry['name']} | {entry['email']} | {entry['event']}")

    except FileNotFoundError as e:
        print(f"\n✗ {e}")
    except ConnectionError as e:
        print(f"\n✗ {e}")
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")


if __name__ == "__main__":
    main()
