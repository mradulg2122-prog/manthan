"""QR Generator Agent - Generates QR codes for pending participants."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.google_sheet_service import GoogleSheetService
from services.qr_service import QRService
from constants import COL_NAME, WORKSHEET_NAME


class QRGeneratorAgent:
    """Generates QR codes for participants who don't have one yet."""

    def __init__(self):
        self.sheet_service = GoogleSheetService()
        self.qr_service = QRService()

    def connect(self, worksheet_name=WORKSHEET_NAME):
        """Authenticate and connect to the sheet."""
        self.sheet_service.authenticate()
        self.sheet_service.connect_to_sheet()
        self.sheet_service.open_worksheet(worksheet_name)

    def find_column_index(self, column_name):
        """Find the 1-based column index for a given header name."""
        headers = self.sheet_service.worksheet.row_values(1)
        headers_lower = [h.strip().lower() for h in headers]

        if column_name.strip().lower() not in headers_lower:
            raise ValueError(
                f"Column '{column_name}' not found.\nAvailable: {headers}"
            )
        return headers_lower.index(column_name.strip().lower()) + 1

    def needs_qr(self, row):
        """Check if participant needs a QR code generated."""
        reg_id = str(row.get("registration_id", "")).strip()
        qr_sent = str(row.get("qr_sent", "")).strip().lower()
        return bool(reg_id) and qr_sent not in ("yes",)

    def generate_qr_codes(self, worksheet_name=WORKSHEET_NAME):
        """Generate QR codes for all pending participants."""
        self.connect(worksheet_name)

        # Read all rows
        rows = self.sheet_service.worksheet.get_all_records()
        if not rows:
            print("\n✗ No registrations found in the sheet.")
            return

        print(f"\n✓ Participants loaded: {len(rows)}")

        # Find qr_sent column
        qr_sent_col = self.find_column_index("qr_sent")

        generated_count = 0
        skipped_count = 0

        for index, row in enumerate(rows):
            reg_id = str(row.get("registration_id", "")).strip()

            if not self.needs_qr(row):
                skipped_count += 1
                continue

            # Generate and save QR
            filepath = self.qr_service.save_qr(reg_id)
            name = str(row.get(COL_NAME, "Unknown")).strip()
            print(f"  ✓ QR generated: {reg_id} → {name}")
            print(f"    ✓ QR saved: {filepath}")

            # Update qr_sent column in sheet
            sheet_row = index + 2  # header + 1-based
            try:
                self.sheet_service.worksheet.update_cell(sheet_row, qr_sent_col, "Yes")
            except Exception as e:
                raise ConnectionError(f"Failed to update qr_sent for {reg_id}: {e}")

            generated_count += 1

        print(f"\n✓ QR codes generated: {generated_count}")
        print(f"✓ Already had QR: {skipped_count}")
        if generated_count > 0:
            print(f"✓ Google Sheet updated")


def main():
    """Test the QR Generator Agent."""
    agent = QRGeneratorAgent()

    try:
        agent.generate_qr_codes()
    except FileNotFoundError as e:
        print(f"\n✗ {e}")
    except ConnectionError as e:
        print(f"\n✗ {e}")
    except ValueError as e:
        print(f"\n✗ {e}")
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")


if __name__ == "__main__":
    main()
