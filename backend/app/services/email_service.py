"""
Email Service.
Sends emails with QR code attachments via Gmail API (OAuth 2.0).

Uses HTTPS (port 443), so it works on Render and all platforms
without SMTP port restrictions.
"""

import os
import base64
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from app.config import settings

logger = logging.getLogger("eventflow.email")

# Gmail API scope — only needs permission to send emails
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
TOKEN_URI = "https://oauth2.googleapis.com/token"


def _get_gmail_service():
    """Build and return an authenticated Gmail API service object."""

    if not settings.GMAIL_CLIENT_ID:
        raise ValueError("GMAIL_CLIENT_ID is not set in environment variables.")
    if not settings.GMAIL_CLIENT_SECRET:
        raise ValueError("GMAIL_CLIENT_SECRET is not set in environment variables.")
    if not settings.GMAIL_REFRESH_TOKEN:
        raise ValueError("GMAIL_REFRESH_TOKEN is not set in environment variables.")

    creds = Credentials(
        token=None,
        refresh_token=settings.GMAIL_REFRESH_TOKEN,
        token_uri=TOKEN_URI,
        client_id=settings.GMAIL_CLIENT_ID,
        client_secret=settings.GMAIL_CLIENT_SECRET,
        scopes=SCOPES,
    )

    # Refresh the access token automatically using the refresh token
    creds.refresh(Request())
    logger.info("  Gmail OAuth token refreshed successfully.")

    service = build("gmail", "v1", credentials=creds, cache_discovery=False)
    return service


def send_qr_email(
    recipient_email: str,
    recipient_name: str,
    registration_id: str,
    qr_image_path: str,
    event_name: str = "EventFlow Pro",
) -> None:
    """Send a registration confirmation email with QR code attached via Gmail API."""

    # --- Pre-flight checks ---
    if not os.path.exists(qr_image_path):
        logger.error("QR image not found: %s", qr_image_path)
        raise FileNotFoundError(f"QR image not found: {qr_image_path}")

    sender_email = settings.GMAIL_SENDER_EMAIL

    # --- Build the MIME email ---
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = f"{event_name} — Registration Confirmed"

    body = (
        f"Hello {recipient_name},\n\n"
        f"Thank you for registering for {event_name}.\n\n"
        f"Your registration has been confirmed.\n\n"
        f"Your Registration ID: {registration_id}\n\n"
        f"Please find your QR Code attached.\n\n"
        f"Carry this QR Code on the event day.\n\n"
        f"Regards,\n"
        f"EventFlow Team"
    )
    msg.attach(MIMEText(body, "plain"))

    # --- Attach QR image ---
    with open(qr_image_path, "rb") as f:
        qr_img = MIMEImage(f.read(), name=f"{registration_id}.png")
        qr_img.add_header(
            "Content-Disposition", "attachment",
            filename=f"{registration_id}.png",
        )
        msg.attach(qr_img)

    # --- Send via Gmail API ---
    try:
        logger.info("  Authenticating with Gmail API...")
        service = _get_gmail_service()

        raw_message = base64.urlsafe_b64encode(msg.as_bytes()).decode("utf-8")

        logger.info("  Sending email from %s to %s ...", sender_email, recipient_email)
        result = service.users().messages().send(
            userId="me",
            body={"raw": raw_message},
        ).execute()

        message_id = result.get("id", "unknown")
        logger.info("  Email sent via Gmail API. Message ID: %s", message_id)

    except HttpError as e:
        logger.error("  Gmail API HTTP Error: %s", e)
        raise
    except Exception as e:
        logger.error("  Gmail API Error: %s", e)
        raise
