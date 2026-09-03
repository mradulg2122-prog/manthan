"""
Batch script to send Thank You + Saturangle Club Hiring emails
to all participants marked as 'Present' in MANTHAN.
"""
import os
import sys
import time
import logging

sys.stdout.reconfigure(encoding='utf-8')

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from dotenv import load_dotenv
load_dotenv(os.path.join(backend_dir, ".env"))

from app.database.database import SessionLocal
from app.models.participant import Participant
from app.services.email_service import send_thankyou_email

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger("eventflow.thankyou_batch")

def dispatch_thankyou_emails():
    db = SessionLocal()
    try:
        present_participants = (
            db.query(Participant)
            .filter(Participant.attendance_status == "Present")
            .all()
        )
        
        total = len(present_participants)
        print(f"[*] Found {total} participant(s) marked as 'Present'.")
        
        if total == 0:
            print("[INFO] No participants currently marked as 'Present'. Mark attendance first.")
            return

        success_count = 0
        failed_count = 0

        for idx, p in enumerate(present_participants, 1):
            print(f"[{idx}/{total}] Sending Thank You email to: {p.name} <{p.email}> (ID: {p.registration_id})...")
            try:
                send_thankyou_email(
                    recipient_email=p.email,
                    recipient_name=p.name,
                )
                success_count += 1
                print(f"  -> [OK] Dispatched to {p.email}")
                time.sleep(0.5)  # small spacing to avoid rate limiting
            except Exception as e:
                failed_count += 1
                print(f"  -> [FAILED] Error sending to {p.email}: {e}")

        print("\n==========================================")
        print(f"Summary: Total: {total} | Dispatched: {success_count} | Failed: {failed_count}")
        print("==========================================")
    finally:
        db.close()

if __name__ == "__main__":
    dispatch_thankyou_emails()
