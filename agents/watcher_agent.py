"""Watcher Agent - Autonomous pipeline that processes new Google Form responses."""

import sys
import os
import json
import time
import signal
from collections import deque
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.google_sheet_service import GoogleSheetService
from services.registration_id_service import RegistrationIDService
from services.qr_service import QRService
from services.email_service import EmailService
from config import QR_OUTPUT_DIR, EVENT_NAME, GENERATED_DIR
from constants import (
    COL_REGISTRATION_ID, COL_NAME, COL_EMAIL,
    WORKSHEET_NAME, REGISTRATION_ID_PREFIX,
)

# ── Paths ─────────────────────────────────────────────────────
STATE_FILE = os.path.join(str(GENERATED_DIR), "system", "state.json")

# ── Polling Config ────────────────────────────────────────────
POLL_FAST = 5        # seconds - when queue has items or recent activity
POLL_SLOW = 30       # seconds - when idle for 5+ minutes
IDLE_THRESHOLD = 300  # 5 minutes in seconds

# ── Colors ────────────────────────────────────────────────────
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"


class WatcherAgent:
    """Watches Google Sheet for new form responses and processes them autonomously."""

    def __init__(self):
        self.sheet_service = GoogleSheetService()
        self.id_service = RegistrationIDService()
        self.qr_service = QRService()
        self.email_service = None  # Lazy init
        self.queue = deque()
        self.processing = False  # Worker lock
        self.running = True
        self.last_activity_time = time.time()
        self.poll_interval = POLL_FAST

        # Column indices (cached after first connect)
        self._col_indices = {}

    # ── State Management ──────────────────────────────────────

    def load_state(self):
        """Load last_processed_row from state.json."""
        os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
        if os.path.exists(STATE_FILE):
            try:
                with open(STATE_FILE, "r") as f:
                    return json.load(f)
            except Exception:
                pass
        return {"last_processed_row": 0}

    def save_state(self, state):
        """Save state to state.json immediately."""
        os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
        with open(STATE_FILE, "w") as f:
            json.dump(state, f, indent=4)

    # ── Connection ────────────────────────────────────────────

    def connect(self):
        """Authenticate and connect to the worksheet."""
        self.sheet_service.authenticate()
        self.sheet_service.connect_to_sheet()
        self.sheet_service.open_worksheet(WORKSHEET_NAME)
        self._cache_column_indices()

    def reconnect(self):
        """Reconnect after an error."""
        self.sheet_service.client = None
        self.sheet_service.spreadsheet = None
        self.sheet_service.worksheet = None
        self._col_indices = {}
        self.connect()

    def _cache_column_indices(self):
        """Cache column indices for fast lookup."""
        headers = self.sheet_service.worksheet.row_values(1)
        headers_lower = [h.strip().lower() for h in headers]
        self._col_indices = {}
        for i, h in enumerate(headers_lower):
            self._col_indices[h] = i + 1  # 1-based

    def _col(self, name):
        """Get 1-based column index by header name."""
        return self._col_indices.get(name.strip().lower())

    # ── Polling ───────────────────────────────────────────────

    def check_new_rows(self, last_row):
        """Read only rows after last_processed_row. Returns list of (sheet_row, row_data)."""
        all_values = self.sheet_service.worksheet.get_all_values()
        total_rows = len(all_values) - 1  # exclude header

        if total_rows <= last_row:
            return []

        headers = all_values[0]
        new_rows = []
        for i in range(last_row + 1, total_rows + 1):
            row_values = all_values[i]
            row_dict = {}
            for j, header in enumerate(headers):
                row_dict[header.strip()] = row_values[j] if j < len(row_values) else ""
            sheet_row = i + 1  # 1-based (header is row 1)
            new_rows.append((sheet_row, row_dict))

        return new_rows

    # ── Validation ────────────────────────────────────────────

    def should_process(self, row_data):
        """Check if a row needs processing. Skip already-completed or invalid rows."""
        name = str(row_data.get(COL_NAME, "")).strip()
        email = str(row_data.get(COL_EMAIL, "")).strip()

        # Skip invalid rows
        if not name or not email:
            return False, "missing name or email"

        reg_id = str(row_data.get("registration_id", "")).strip()
        qr_sent = str(row_data.get("qr_sent", "")).strip().lower()
        email_sent = str(row_data.get("email_sent", "")).strip().lower()

        # Skip fully processed
        if reg_id and qr_sent == "yes" and email_sent == "yes":
            return False, "already completed"

        return True, "needs processing"

    # ── Per-Participant Pipeline ──────────────────────────────

    def process_participant(self, sheet_row, row_data):
        """Run the full pipeline for a single participant."""
        name = str(row_data.get(COL_NAME, "")).strip()
        email = str(row_data.get(COL_EMAIL, "")).strip()
        reg_id = str(row_data.get("registration_id", "")).strip()

        # Step 1: Generate Registration ID
        if not reg_id:
            reg_id = self._assign_registration_id(sheet_row)
            if not reg_id:
                return False
            self._log(f"  ID assigned: {reg_id}", GREEN)

        # Step 2: Generate QR Code
        qr_sent = str(row_data.get("qr_sent", "")).strip().lower()
        if qr_sent != "yes":
            try:
                filepath = self.qr_service.save_qr(reg_id)
                qr_col = self._col("qr_sent")
                if qr_col:
                    self.sheet_service.worksheet.update_cell(sheet_row, qr_col, "Yes")
                self._log(f"  QR saved: {filepath}", GREEN)
            except Exception as e:
                self._log(f"  QR failed: {e}", RED)
                return False

        # Step 3: Send Email
        email_sent = str(row_data.get("email_sent", "")).strip().lower()
        if email_sent != "yes":
            try:
                if not self.email_service:
                    self.email_service = EmailService()

                qr_path = os.path.join(str(QR_OUTPUT_DIR), f"{reg_id}.png")
                self.email_service.send_qr_email(email, name, reg_id, qr_path, EVENT_NAME)

                email_col = self._col("email_sent")
                if email_col:
                    self.sheet_service.worksheet.update_cell(sheet_row, email_col, "Yes")
                self._log(f"  Email sent: {email}", GREEN)
            except ValueError as e:
                self._log(f"  Email skipped (SMTP not configured): {e}", YELLOW)
            except Exception as e:
                self._log(f"  Email failed: {e}", RED)
                return False

        return True

    def _assign_registration_id(self, sheet_row):
        """Generate and write a registration ID for a specific row."""
        try:
            # Read all existing IDs to find next sequence
            all_rows = self.sheet_service.worksheet.get_all_records()
            existing_ids = self.id_service.extract_existing_ids(all_rows)
            last_num = self.id_service.get_last_number(existing_ids)
            new_id = self.id_service.generate_id(last_num + 1)

            # Write to sheet
            reg_col = self._col("registration_id")
            if reg_col:
                self.sheet_service.worksheet.update_cell(sheet_row, reg_col, new_id)
            return new_id
        except Exception as e:
            self._log(f"  ID generation failed: {e}", RED)
            return None

    # ── Worker ────────────────────────────────────────────────

    def process_queue(self):
        """Process all items in the queue sequentially. Single worker only."""
        if self.processing:
            return  # Lock: prevent parallel processing

        self.processing = True
        state = self.load_state()

        try:
            total = len(self.queue)
            count = 0

            while self.queue and self.running:
                sheet_row, row_data = self.queue.popleft()
                count += 1
                name = str(row_data.get(COL_NAME, "")).strip()

                self._log(f"Processing {count}/{total}: {name} (row {sheet_row})", CYAN)

                should, reason = self.should_process(row_data)
                if not should:
                    self._log(f"  Skipped: {reason}", YELLOW)
                    state["last_processed_row"] = max(state["last_processed_row"], sheet_row - 1)
                    self.save_state(state)
                    continue

                success = False
                retries = 3
                for attempt in range(retries):
                    try:
                        success = self.process_participant(sheet_row, row_data)
                        break
                    except Exception as e:
                        self._log(f"  Attempt {attempt + 1}/{retries} failed: {e}", RED)
                        if attempt < retries - 1:
                            time.sleep(5)
                            try:
                                self.reconnect()
                                self._log("  Reconnected", GREEN)
                            except Exception:
                                pass

                if success:
                    self._log(f"  Completed", GREEN)
                else:
                    self._log(f"  Failed after {retries} attempts", RED)

                # Update state after every participant (success or fail)
                state["last_processed_row"] = max(state["last_processed_row"], sheet_row - 1)
                self.save_state(state)

        finally:
            self.processing = False

    # ── Adaptive Polling ──────────────────────────────────────

    def update_poll_interval(self, found_new):
        """Adjust polling speed based on activity."""
        if found_new:
            self.last_activity_time = time.time()
            self.poll_interval = POLL_FAST
        else:
            idle_time = time.time() - self.last_activity_time
            if idle_time > IDLE_THRESHOLD:
                self.poll_interval = POLL_SLOW
            else:
                self.poll_interval = POLL_FAST

    # ── Main Loop ─────────────────────────────────────────────

    def watch(self):
        """Main watch loop. Runs forever until Ctrl+C."""
        self._print_banner()

        # Connect
        try:
            self.connect()
            self._log("Connected to Google Sheet", GREEN)
        except Exception as e:
            self._log(f"Connection failed: {e}", RED)
            return

        state = self.load_state()
        self._log(f"Resuming from row: {state['last_processed_row']}", CYAN)
        self._log("Watching...\n", GREEN)

        while self.running:
            try:
                # Poll for new rows
                new_rows = self.check_new_rows(state["last_processed_row"])

                if new_rows:
                    self._log(f"New registrations found: {len(new_rows)}", CYAN)

                    # Add to queue
                    for item in new_rows:
                        self.queue.append(item)

                    self._log(f"Queue size: {len(self.queue)}", CYAN)

                    # Process queue (single worker)
                    self.process_queue()

                    # Reload state after processing
                    state = self.load_state()
                    self.update_poll_interval(found_new=True)
                else:
                    self.update_poll_interval(found_new=False)
                    interval_label = f"{self.poll_interval}s"
                    now = datetime.now().strftime("%H:%M:%S")
                    print(f"{DIM}  [{now}] Waiting... (poll: {interval_label}){RESET}", end="\r")

                # Sleep with interrupt support
                for _ in range(self.poll_interval):
                    if not self.running:
                        break
                    time.sleep(1)

            except KeyboardInterrupt:
                break
            except Exception as e:
                self._log(f"Error: {e}", RED)
                self._log("Retrying in 10 seconds...", YELLOW)
                time.sleep(10)

                # Attempt reconnect
                try:
                    self.reconnect()
                    self._log("Reconnected", GREEN)
                except Exception:
                    self._log("Reconnect failed, will retry next cycle", RED)

    # ── Shutdown ──────────────────────────────────────────────

    def shutdown(self, signum=None, frame=None):
        """Graceful shutdown: finish current, save state, exit."""
        print()  # New line after \r
        self._log("Shutting down...", YELLOW)
        self.running = False

    # ── Logging ───────────────────────────────────────────────

    def _log(self, message, color=RESET):
        """Print a timestamped colored log."""
        now = datetime.now().strftime("%H:%M:%S")
        symbol = "+" if color == GREEN else "!" if color == RED else "~" if color == YELLOW else ">"
        print(f"{color}{symbol} [{now}] {message}{RESET}")

    def _print_banner(self):
        """Print the watcher startup banner."""
        print(f"""
{CYAN}{BOLD}========================================
       EventFlow AI - Watcher
     Autonomous Registration Pipeline
========================================{RESET}
""")


# ── Main ──────────────────────────────────────────────────────

def main():
    """Start the autonomous watcher."""
    watcher = WatcherAgent()

    # Register Ctrl+C handler
    signal.signal(signal.SIGINT, watcher.shutdown)

    try:
        watcher.watch()
    finally:
        # Save state on exit
        state = watcher.load_state()
        watcher.save_state(state)
        watcher._log("State saved. Goodbye!", GREEN)


if __name__ == "__main__":
    main()
