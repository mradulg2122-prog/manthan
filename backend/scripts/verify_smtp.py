"""
SMTP Verification & Diagnostic Script for EventFlow Pro.
Run:
    python scripts/verify_smtp.py
"""

import os
import sys
import smtplib
import ssl
from dotenv import load_dotenv

# Ensure backend root is in path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_EMAIL = os.getenv("SMTP_EMAIL", "mradulg2122@gmail.com")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "").strip()

print("=" * 60)
print("  EVENTFLOW SMTP DIAGNOSTIC TOOL")
print("=" * 60)
print(f"  SMTP Server : {SMTP_HOST}:{SMTP_PORT}")
print(f"  Sender Email: {SMTP_EMAIL}")
print(f"  Password Set: {'YES (' + '*' * len(SMTP_PASSWORD) + ')' if SMTP_PASSWORD else 'NO (EMPTY)'}")
print("-" * 60)

if not SMTP_PASSWORD:
    print("[!] ERROR: SMTP_PASSWORD is not set in backend/.env!")
    print("\nHow to fix:")
    print("1. Open Google Account: https://myaccount.google.com/security")
    print("2. Ensure '2-Step Verification' is turned ON.")
    print("3. Search for 'App passwords' or visit: https://myaccount.google.com/apppasswords")
    print("4. Create an App password for 'EventFlow' and copy the 16-character code (e.g. abcd efgh ijkl mnop).")
    print("5. Paste it in backend/.env under SMTP_PASSWORD=your_16_char_password")
    sys.exit(1)

print("1. Testing network connection to SMTP server...")
try:
    server = smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10)
    server.ehlo()
    print("   [+] Connected to server successfully.")
except Exception as e:
    print(f"   [!] Connection failed: {e}")
    sys.exit(1)

print("2. Establishing secure TLS encryption...")
try:
    context = ssl.create_default_context()
    server.starttls(context=context)
    server.ehlo()
    print("   [+] TLS encryption established.")
except Exception as e:
    print(f"   [!] TLS failed: {e}")
    server.quit()
    sys.exit(1)

print("3. Authenticating with Gmail credentials...")
try:
    server.login(SMTP_EMAIL, SMTP_PASSWORD)
    print(f"   [+] SUCCESS! Successfully authenticated as {SMTP_EMAIL}")
    server.quit()
    print("\n[SUCCESS] SMTP is configured properly! Confirmation emails with QR codes will now be dispatched automatically.")
except smtplib.SMTPAuthenticationError as e:
    print(f"   [!] Authentication FAILED: {e}")
    print("\n[!] Gmail rejected the password. Please make sure you are using a 16-character Google 'App Password' (not your personal Google account password).")
    server.quit()
    sys.exit(1)
except Exception as e:
    print(f"   [!] Unexpected error: {e}")
    server.quit()
    sys.exit(1)
