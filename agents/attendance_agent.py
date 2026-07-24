"""Attendance Agent - Marks attendance on Google Sheet via scanned QR."""

import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.google_sheet_service import GoogleSheetService
from constants import COL_REGISTRATION_ID, COL_ATTENDANCE_STATUS, COL_CHECK_IN_TIME, COL_NAME, STATUS_CHECKED_IN, WORKSHEET_NAME


# Result constants
RESULT_SUCCESS = "Success"
RESULT_ALREADY_PRESENT = "Already Present"
RESULT_INVALID_QR = "Invalid QR"


class AttendanceAgent:
    """Searches for a registration ID and marks attendance."""

    def __init__(self):
        self.sheet_service = GoogleSheetService()
        self.connected = False
        self._rows_cache = None
        self._headers = None

    def connect(self, worksheet_name=WORKSHEET_NAME):
        """Authenticate and connect to the sheet."""
        if not self.connected:
            self.sheet_service.authenticate()
            self.sheet_service.connect_to_sheet()
            self.sheet_service.open_worksheet(worksheet_name)
            self._headers = self.sheet_service.worksheet.row_values(1)
            self.connected = True

    def find_column_index(self, column_name):
        """Find the 1-based column index for a header name."""
        headers_lower = [h.strip().lower() for h in self._headers]
        key = column_name.strip().lower()
        if key not in headers_lower:
            raise ValueError(f"Column '{column_name}' not found.\nAvailable: {self._headers}")
        return headers_lower.index(key) + 1

    def find_participant_row(self, registration_id):
        """Find the sheet row number for a registration ID. Returns (row_number, row_data) or (None, None)."""
        rows = self.sheet_service.worksheet.get_all_records()

        for index, row in enumerate(rows):
            reg_id = str(row.get("registration_id", "")).strip()
            if reg_id == registration_id:
                sheet_row = index + 2  # header + 1-based
                return sheet_row, row

        return None, None

    def mark_attendance(self, registration_id):
        """Mark attendance for a registration ID. Returns result string."""
        self.connect()

        sheet_row, row_data = self.find_participant_row(registration_id)

        # Not found
        if sheet_row is None:
            print(f"  ✗ Invalid QR Code: {registration_id}")
            return RESULT_INVALID_QR

        name = str(row_data.get(COL_NAME, "Unknown")).strip()
        current_status = str(row_data.get(COL_ATTENDANCE_STATUS, "")).strip()

        # Already checked in
        if current_status == STATUS_CHECKED_IN:
            print(f"  ⚠ Already Checked In: {registration_id} ({name})")
            return RESULT_ALREADY_PRESENT

        # Mark as present
        try:
            status_col = self.find_column_index(COL_ATTENDANCE_STATUS)
            time_col = self.find_column_index(COL_CHECK_IN_TIME)
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            self.sheet_service.worksheet.update_cell(sheet_row, status_col, STATUS_CHECKED_IN)
            self.sheet_service.worksheet.update_cell(sheet_row, time_col, now)

            print(f"  ✓ Participant Found: {name}")
            print(f"  ✓ Attendance Updated: {registration_id} at {now}")
            return RESULT_SUCCESS

        except Exception as e:
            raise ConnectionError(f"Failed to update attendance for {registration_id}: {e}")


def main():
    """Test the Attendance Agent with a manual ID."""
    agent = AttendanceAgent()

    test_id = input("\nEnter registration ID to test: ").strip()
    if not test_id:
        print("✗ No ID entered.")
        return

    try:
        result = agent.mark_attendance(test_id)
        print(f"\nResult: {result}")
    except FileNotFoundError as e:
        print(f"\n✗ {e}")
    except ConnectionError as e:
        print(f"\n✗ {e}")
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")


if __name__ == "__main__":
    main()
