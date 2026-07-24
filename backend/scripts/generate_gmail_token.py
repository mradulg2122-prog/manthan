"""
Gmail OAuth 2.0 Refresh Token Generator.

Usage:
  cd EventFlow_AI
  python backend/scripts/generate_gmail_token.py

Prerequisites:
  1. Enable Gmail API at: https://console.cloud.google.com/apis/library/gmail.googleapis.com
  2. credentials/credentials.json must exist (OAuth Desktop App client)
  3. Add mradulg2122@gmail.com as a test user in OAuth consent screen
"""

import os
import sys
import json
import webbrowser

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))
CLIENT_SECRET_FILE = os.path.join(PROJECT_ROOT, "credentials", "credentials.json")

from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


def main():
    print("=" * 60)
    print("  Gmail API - Refresh Token Generator")
    print("=" * 60)

    if not os.path.exists(CLIENT_SECRET_FILE):
        print(f"\nERROR: {CLIENT_SECRET_FILE} not found.")
        sys.exit(1)

    with open(CLIENT_SECRET_FILE) as f:
        client_data = json.load(f)
        installed = client_data.get("installed", client_data.get("web", {}))
        client_id = installed.get("client_id", "")
        client_secret = installed.get("client_secret", "")

    print(f"\nUsing: {CLIENT_SECRET_FILE}")
    print(f"Client ID: {client_id[:20]}...")
    print(f"\nStarting local OAuth server on port 8090...")
    print(f"Your browser should open automatically.")
    print(f"If it doesn't, open this URL manually after the server starts.\n")

    flow = InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRET_FILE,
        scopes=SCOPES,
    )

    creds = flow.run_local_server(
        port=8090,
        prompt="consent",
        access_type="offline",
        open_browser=True,
    )

    print()
    print("=" * 60)
    print("  SUCCESS! Add these to .env and Render:")
    print("=" * 60)
    print()
    print(f"GMAIL_CLIENT_ID={client_id}")
    print(f"GMAIL_CLIENT_SECRET={client_secret}")
    print(f"GMAIL_REFRESH_TOKEN={creds.refresh_token}")
    print(f"GMAIL_SENDER_EMAIL=mradulg2122@gmail.com")
    print()
    print("=" * 60)


if __name__ == "__main__":
    main()
