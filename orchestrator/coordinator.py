"""Coordinator - LangGraph workflow for the full registration pipeline."""

import sys
import os
from typing import TypedDict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langgraph.graph import StateGraph, START, END

from services.google_sheet_service import GoogleSheetService
from services.registration_id_service import RegistrationIDService
from services.qr_service import QRService
from services.email_service import EmailService
from agents.logger_agent import LoggerAgent
from config import QR_OUTPUT_DIR, EVENT_NAME
from constants import COL_REGISTRATION_ID, COL_NAME, COL_EMAIL, WORKSHEET_NAME

# Shared logger
logger = LoggerAgent()


# ── Workflow State ────────────────────────────────────────────
class WorkflowState(TypedDict):
    participants_processed: int
    ids_generated: int
    qr_generated: int
    emails_sent: int
    failed: int
    errors: list


# ── Node Functions ────────────────────────────────────────────

def load_registrations(state: WorkflowState) -> WorkflowState:
    """Node 1: Load all registrations from Google Sheet."""
    logger.step("REGISTRATION AGENT")

    try:
        sheet = GoogleSheetService()
        sheet.authenticate()
        sheet.connect_to_sheet()
        sheet.open_worksheet(WORKSHEET_NAME)
        rows = sheet.worksheet.get_all_records()

        valid = [r for r in rows if str(r.get(COL_NAME, "")).strip() and str(r.get(COL_EMAIL, "")).strip()]

        logger.info(f"Total rows: {len(rows)}")
        logger.info(f"Valid participants: {len(valid)}")

        state["participants_processed"] = len(valid)

    except Exception as e:
        logger.error(f"Registration load failed: {e}")
        state["errors"].append(f"Registration: {e}")
        state["failed"] += 1

    return state


def generate_ids(state: WorkflowState) -> WorkflowState:
    """Node 2: Assign registration IDs to participants without one."""
    logger.step("ID GENERATOR AGENT")

    try:
        sheet = GoogleSheetService()
        sheet.authenticate()
        sheet.connect_to_sheet()
        sheet.open_worksheet(WORKSHEET_NAME)
        rows = sheet.worksheet.get_all_records()

        id_service = RegistrationIDService()
        assignments, all_ids = id_service.generate_new_ids(rows)

        if not assignments:
            logger.info("All participants already have IDs")
            return state

        # Find registration_id column
        headers = sheet.worksheet.row_values(1)
        headers_lower = [h.strip().lower() for h in headers]
        col_index = headers_lower.index(COL_REGISTRATION_ID) + 1

        for data_index, new_id in assignments:
            try:
                sheet_row = data_index + 2
                sheet.worksheet.update_cell(sheet_row, col_index, new_id)
                name = str(rows[data_index].get(COL_NAME, "")).strip()
                logger.info(f"ID assigned: {new_id} → {name}")
                state["ids_generated"] += 1
            except Exception as e:
                logger.error(f"ID update failed for row {data_index}: {e}")
                state["failed"] += 1
                state["errors"].append(f"ID: {e}")

    except Exception as e:
        logger.error(f"ID generation failed: {e}")
        state["errors"].append(f"ID: {e}")
        state["failed"] += 1

    return state


def generate_qr_codes(state: WorkflowState) -> WorkflowState:
    """Node 3: Generate QR codes for pending participants."""
    logger.step("QR GENERATOR AGENT")

    try:
        sheet = GoogleSheetService()
        sheet.authenticate()
        sheet.connect_to_sheet()
        sheet.open_worksheet(WORKSHEET_NAME)
        rows = sheet.worksheet.get_all_records()

        # Find qr_sent column
        headers = sheet.worksheet.row_values(1)
        headers_lower = [h.strip().lower() for h in headers]
        qr_sent_col = headers_lower.index("qr_sent") + 1

        qr_service = QRService()

        for index, row in enumerate(rows):
            reg_id = str(row.get("registration_id", "")).strip()
            qr_sent = str(row.get("qr_sent", "")).strip().lower()

            if not reg_id or qr_sent == "yes":
                continue

            try:
                filepath = qr_service.save_qr(reg_id)
                sheet_row = index + 2
                sheet.worksheet.update_cell(sheet_row, qr_sent_col, "Yes")
                logger.info(f"QR saved: {reg_id} → {filepath}")
                state["qr_generated"] += 1
            except Exception as e:
                logger.error(f"QR failed for {reg_id}: {e}")
                state["failed"] += 1
                state["errors"].append(f"QR {reg_id}: {e}")

    except Exception as e:
        logger.error(f"QR generation failed: {e}")
        state["errors"].append(f"QR: {e}")
        state["failed"] += 1

    return state


def send_emails(state: WorkflowState) -> WorkflowState:
    """Node 4: Send QR code emails to pending participants."""
    logger.step("EMAIL QR AGENT")

    try:
        email_service = EmailService()
    except ValueError as e:
        logger.warning(f"Email skipped: {e}")
        state["errors"].append(f"Email: {e}")
        return state

    try:
        sheet = GoogleSheetService()
        sheet.authenticate()
        sheet.connect_to_sheet()
        sheet.open_worksheet(WORKSHEET_NAME)
        rows = sheet.worksheet.get_all_records()

        # Find email_sent column
        headers = sheet.worksheet.row_values(1)
        headers_lower = [h.strip().lower() for h in headers]
        email_sent_col = headers_lower.index("email_sent") + 1

        qr_dir = str(QR_OUTPUT_DIR)

        for index, row in enumerate(rows):
            reg_id = str(row.get("registration_id", "")).strip()
            email = str(row.get(COL_EMAIL, "")).strip()
            name = str(row.get(COL_NAME, "")).strip()
            qr_sent = str(row.get("qr_sent", "")).strip().lower()
            email_sent = str(row.get("email_sent", "")).strip().lower()

            if not reg_id or not email or qr_sent != "yes" or email_sent == "yes":
                continue

            qr_path = os.path.join(qr_dir, f"{reg_id}.png")
            if not os.path.exists(qr_path):
                logger.warning(f"QR image missing for {reg_id}")
                continue

            try:
                email_service.send_qr_email(email, name, reg_id, qr_path, EVENT_NAME)
                sheet_row = index + 2
                sheet.worksheet.update_cell(sheet_row, email_sent_col, "Yes")
                logger.info(f"Email sent: {reg_id} → {email}")
                state["emails_sent"] += 1
            except Exception as e:
                logger.error(f"Email failed for {reg_id}: {e}")
                state["failed"] += 1
                state["errors"].append(f"Email {reg_id}: {e}")

    except Exception as e:
        logger.error(f"Email step failed: {e}")
        state["errors"].append(f"Email: {e}")
        state["failed"] += 1

    return state


def log_summary(state: WorkflowState) -> WorkflowState:
    """Node 5: Log the final workflow summary."""
    logger.step("WORKFLOW COMPLETE")

    logger.summary({
        "Participants Processed": state["participants_processed"],
        "IDs Generated": state["ids_generated"],
        "QR Generated": state["qr_generated"],
        "Emails Sent": state["emails_sent"],
        "Failed": state["failed"],
    })

    if state["errors"]:
        logger.warning(f"Errors encountered: {len(state['errors'])}")
        for err in state["errors"]:
            logger.error(f"  → {err}")

    return state


# ── Build LangGraph Workflow ──────────────────────────────────

def build_workflow():
    """Build and compile the LangGraph workflow."""
    graph = StateGraph(WorkflowState)

    # Add nodes
    graph.add_node("load_registrations", load_registrations)
    graph.add_node("generate_ids", generate_ids)
    graph.add_node("generate_qr_codes", generate_qr_codes)
    graph.add_node("send_emails", send_emails)
    graph.add_node("log_summary", log_summary)

    # Add edges: START → registration → ids → qr → email → logger → END
    graph.add_edge(START, "load_registrations")
    graph.add_edge("load_registrations", "generate_ids")
    graph.add_edge("generate_ids", "generate_qr_codes")
    graph.add_edge("generate_qr_codes", "send_emails")
    graph.add_edge("send_emails", "log_summary")
    graph.add_edge("log_summary", END)

    return graph.compile()


# ── Main ──────────────────────────────────────────────────────

def main():
    """Run the full EventFlow AI workflow."""
    logger.step("EVENTFLOW AI - STARTING WORKFLOW")

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
    except Exception as e:
        logger.error(f"Workflow crashed: {e}")


if __name__ == "__main__":
    main()
