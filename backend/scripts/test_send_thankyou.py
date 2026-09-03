"""
Test sending Thank You + Saturangle Club Hiring email to Mradul Gaur.
"""
import os
import sys

# Set stdout encoding
sys.stdout.reconfigure(encoding='utf-8')

# Ensure backend root is in python path
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from dotenv import load_dotenv
load_dotenv(os.path.join(backend_dir, ".env"))

from app.services.email_service import send_thankyou_email

def main():
    test_email = "mradulg2122@gmail.com"
    test_name = "Mradul Gaur"
    print(f"[*] Sending test Thank You email to {test_name} <{test_email}>...")
    try:
        send_thankyou_email(
            recipient_email=test_email,
            recipient_name=test_name,
        )
        print("[SUCCESS] Test Thank You email sent successfully.")
    except Exception as e:
        print(f"[ERROR] sending email: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
