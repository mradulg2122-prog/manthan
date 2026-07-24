"""EventFlow AI - Main Entry Point"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from orchestrator.coordinator import build_workflow, logger, WorkflowState


BANNER = """
\033[96m\033[1m
========================================

        EventFlow AI

 QR Based Smart Attendance System

========================================
\033[0m"""

COMPLETE = """
\033[92m\033[1m
========================================

  Workflow Completed Successfully

========================================
\033[0m"""

FAILED = """
\033[91m\033[1m
========================================

  Workflow Failed - Check Logs

========================================
\033[0m"""


def main():
    """Run the complete EventFlow AI registration workflow."""
    print(BANNER)

    logger.info("EventFlow AI starting...")

    # Build the LangGraph workflow
    workflow = build_workflow()

    initial_state: WorkflowState = {
        "participants_processed": 0,
        "ids_generated": 0,
        "qr_generated": 0,
        "emails_sent": 0,
        "failed": 0,
        "errors": [],
    }

    try:
        result = workflow.invoke(initial_state)

        if result["failed"] == 0:
            print(COMPLETE)
        else:
            print(FAILED)
            logger.warning(f"{result['failed']} error(s) occurred. Check logs/system.log")

        logger.info("EventFlow AI finished.")

    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        print(FAILED)
    except ConnectionError as e:
        logger.error(f"Connection error: {e}")
        print(FAILED)
    except KeyboardInterrupt:
        logger.warning("Interrupted by user.")
        print("\n\033[93m⚠ Workflow interrupted.\033[0m")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(FAILED)


if __name__ == "__main__":
    main()
