"""ID Generator Agent - Assigns registration IDs to participants."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.google_sheet_service import GoogleSheetService
from services.registration_id_service import RegistrationIDService
from constants import COL_REGISTRATION_ID, COL_NAME, WORKSHEET_NAME


class IDGeneratorAgent:
    """Assigns unique IDs to participants who don't have one."""

    def __init__(self):
        self.sheet_service = GoogleSheetService()
        self.id_service = RegistrationIDService()

    def connect(self, worksheet_name=WORKSHEET_NAME):
        """Authenticate and connect to the sheet."""
        self.sheet_service.authenticate()
        self.sheet_service.connect_to_sheet()
        self.sheet_service.open_worksheet(worksheet_name)

    def find_registration_id_column(self):
        """Find the column index of 'registration_id' in the header."""
        headers = self.sheet_service.worksheet.row_values(1)
        headers_lower = [h.strip().lower() for h in headers]

        if COL_REGISTRATION_ID not in headers_lower:
            raise ValueError(
                f"Column '{COL_REGISTRATION_ID}' not found in sheet.\n"
                f"Available columns: {headers}"
            )

        # gspread uses 1-based column index
        return headers_lower.index(COL_REGISTRATION_ID) + 1

    def assign_ids(self, worksheet_name=WORKSHEET_NAME):
        """Read registrations, generate IDs, and update the sheet."""
        self.connect(worksheet_name)

        # Read all rows
        rows = self.sheet_service.worksheet.get_all_records()
        if not rows:
            print("\n✗ No registrations found in the sheet.")
            return

        # Generate new IDs
        assignments, all_ids = self.id_service.generate_new_ids(rows)
        existing_count = len(all_ids) - len(assignments)

        print(f"\n✓ Connected to Google Sheet")
        print(f"✓ Total registrations: {len(rows)}")
        print(f"✓ Existing IDs found: {existing_count}")

        if not assignments:
            print(f"✓ All participants already have IDs. Nothing to update.")
            return

        # Find the registration_id column
        col_index = self.find_registration_id_column()

        # Update each row in the sheet
        try:
            for data_index, new_id in assignments:
                # Sheet row = data_index + 2 (row 1 is header, data starts at row 2)
                sheet_row = data_index + 2
                self.sheet_service.worksheet.update_cell(sheet_row, col_index, new_id)

            print(f"✓ New IDs generated: {len(assignments)}")
            print(f"✓ Google Sheet updated")

            # Preview assigned IDs
            print(f"\n--- Assigned IDs ---")
            for data_index, new_id in assignments:
                name = str(rows[data_index].get(COL_NAME, "Unknown")).strip()
                print(f"  {new_id} → {name}")

        except Exception as e:
            raise ConnectionError(f"Failed to update sheet: {e}")


def main():
    """Test the ID Generator Agent."""
    agent = IDGeneratorAgent()

    try:
        agent.assign_ids()
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
