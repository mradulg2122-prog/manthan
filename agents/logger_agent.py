"""Logger Agent - Colored console logs and file logging."""

import os
import sys
import logging
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import LOGS_DIR
from constants import LOG_FILE

# ANSI color codes
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"


class LoggerAgent:
    """Logs workflow steps to console (colored) and file."""

    def __init__(self):
        self.log_dir = str(LOGS_DIR)
        self.log_file = os.path.join(self.log_dir, LOG_FILE)
        self._setup()

    def _setup(self):
        """Create logs folder and configure file logger."""
        os.makedirs(self.log_dir, exist_ok=True)

        self.logger = logging.getLogger("EventFlowAI")
        self.logger.setLevel(logging.DEBUG)

        # Avoid duplicate handlers
        if not self.logger.handlers:
            handler = logging.FileHandler(self.log_file, encoding="utf-8")
            handler.setLevel(logging.DEBUG)
            formatter = logging.Formatter(
                "%(asctime)s | %(levelname)-7s | %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def _timestamp(self):
        """Current timestamp string."""
        return datetime.now().strftime("%H:%M:%S")

    def info(self, message):
        """Log info message."""
        try:
            print(f"{GREEN}✓ [{self._timestamp()}] {message}{RESET}")
            self.logger.info(message)
        except Exception:
            pass  # Never crash

    def warning(self, message):
        """Log warning message."""
        try:
            print(f"{YELLOW}⚠ [{self._timestamp()}] {message}{RESET}")
            self.logger.warning(message)
        except Exception:
            pass

    def error(self, message):
        """Log error message."""
        try:
            print(f"{RED}✗ [{self._timestamp()}] {message}{RESET}")
            self.logger.error(message)
        except Exception:
            pass

    def step(self, step_name):
        """Log a workflow step header."""
        try:
            print(f"\n{CYAN}{BOLD}━━━ {step_name} ━━━{RESET}")
            self.logger.info(f"STEP: {step_name}")
        except Exception:
            pass

    def summary(self, stats):
        """Log workflow summary."""
        try:
            print(f"\n{BOLD}{'═' * 40}{RESET}")
            print(f"{BOLD}  WORKFLOW SUMMARY{RESET}")
            print(f"{BOLD}{'═' * 40}{RESET}")
            for key, value in stats.items():
                color = RED if key == "Failed" and value > 0 else GREEN
                print(f"  {color}{key:<25}: {value}{RESET}")
            print(f"{BOLD}{'═' * 40}{RESET}\n")

            self.logger.info("WORKFLOW SUMMARY: " + str(stats))
        except Exception:
            pass


def main():
    """Test the Logger Agent."""
    logger = LoggerAgent()
    logger.step("Test Step")
    logger.info("This is an info message")
    logger.warning("This is a warning")
    logger.error("This is an error")
    logger.summary({"Processed": 5, "Success": 4, "Failed": 1})
    print(f"\nLog file: {logger.log_file}")


if __name__ == "__main__":
    main()
