"""Registration ID Service - Generates unique registration IDs."""

from datetime import datetime
from constants import REGISTRATION_ID_PREFIX


class RegistrationIDService:
    """Generates and manages unique registration IDs."""

    def __init__(self):
        self.prefix = REGISTRATION_ID_PREFIX
        self.year = datetime.now().strftime("%Y")

    def extract_existing_ids(self, rows):
        """Extract all existing registration IDs from sheet rows."""
        existing = []
        for row in rows:
            reg_id = str(row.get("registration_id", "")).strip()
            if reg_id:
                existing.append(reg_id)
        return existing

    def get_last_number(self, existing_ids):
        """Find the highest sequence number from existing IDs."""
        max_num = 0
        prefix_year = f"{self.prefix}{self.year}"

        for reg_id in existing_ids:
            if reg_id.startswith(prefix_year):
                try:
                    num = int(reg_id[len(prefix_year):])
                    max_num = max(max_num, num)
                except ValueError:
                    continue
        return max_num

    def generate_id(self, sequence_number):
        """Generate a single ID like EVT20260001."""
        return f"{self.prefix}{self.year}{sequence_number:04d}"

    def generate_new_ids(self, rows):
        """Generate IDs for rows that don't have one. Returns list of (row_index, new_id)."""
        existing_ids = self.extract_existing_ids(rows)
        last_number = self.get_last_number(existing_ids)
        assignments = []

        for index, row in enumerate(rows):
            reg_id = str(row.get("registration_id", "")).strip()
            if not reg_id:
                last_number += 1
                new_id = self.generate_id(last_number)

                # Prevent duplicates
                if new_id in existing_ids:
                    raise ValueError(f"Duplicate ID detected: {new_id}")

                existing_ids.append(new_id)
                # row_index is 0-based from data; sheet row = index + 2 (header + 1-based)
                assignments.append((index, new_id))

        return assignments, existing_ids
