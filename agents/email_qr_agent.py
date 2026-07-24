"""Email QR Agent - Emails QR codes to participants who haven't received them."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.google_sheet_service import GoogleSheetService
from services.email_service import EmailService
from constants import COL_NAME, COL_EMAIL, WORKSHEET_NAME
from config import QR_OUTPUT_DIR, EVENT_NAME


class EmailQRAgent:
    """Sends QR code emails to participants and updates the sheet."""

    def __init__(self):
        self.sheet_service = GoogleSheetService()
        self.email_service = EmailService()
        self.qr_dir = str(QR_OUTPUT_DIR)

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

    def needs_email(self, row):
        """Check if participant needs a QR email."""
        reg_id = str(row.get("registration_id", "")).strip()
        email = str(row.get(COL_EMAIL, "")).strip()
        qr_sent = str(row.get("qr_sent", "")).strip().lower()
        email_sent = str(row.get("email_sent", "")).strip().lower()

        # Must have ID, email, QR already generated, and email not yet sent
        return bool(reg_id) and bool(email) and qr_sent == "yes" and email_sent not in ("yes",)

    def send_qr_emails(self, worksheet_name=WORKSHEET_NAME):
        """Send QR code emails to all pending participants."""
        self.connect(worksheet_name)

        rows = self.sheet_service.worksheet.get_all_records()
        if not rows:
            print("\n✗ No registrations found.")
            return

        print(f"\n✓ Participants loaded: {len(rows)}")

        email_sent_col = self.find_column_index("email_sent")

        sent_count = 0
        skipped_count = 0
        failed_count = 0

        for index, row in enumerate(rows):
            if not self.needs_email(row):
                skipped_count += 1
                continue

            reg_id = str(row.get("registration_id", "")).strip()
            name = str(row.get(COL_NAME, "")).strip()
            email = str(row.get(COL_EMAIL, "")).strip()
            qr_path = os.path.join(self.qr_dir, f"{reg_id}.png")

            # Check QR image exists
            if not os.path.exists(qr_path):
                print(f"  ✗ QR image missing for {reg_id}, skipping")
                failed_count += 1
                continue

            # Send email
            try:
                self.email_service.send_qr_email(email, name, reg_id, qr_path, EVENT_NAME)
                print(f"  ✓ Email sent: {reg_id} → {email}")

                # Update email_sent column
                sheet_row = index + 2
                self.sheet_service.worksheet.update_cell(sheet_row, email_sent_col, "Yes")
                sent_count += 1

            except Exception as e:
                print(f"  ✗ Failed for {reg_id} ({email}): {e}")
                failed_count += 1

        print(f"\n✓ Emails sent: {sent_count}")
        print(f"✓ Skipped (already sent): {skipped_count}")
        if failed_count:
            print(f"✗ Failed: {failed_count}")
        if sent_count > 0:
            print(f"✓ Google Sheet updated")


def main():
    """Test the Email QR Agent."""
    agent = EmailQRAgent()

    try:
        agent.send_qr_emails()
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
