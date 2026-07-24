"""
Email Service.
Sends emails with QR code attachments.

Uses Resend HTTP API when RESEND_API_KEY is set (required for Render/production).
Falls back to direct SMTP when RESEND_API_KEY is empty (local development).
"""

import os
import base64
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

from app.config import settings

logger = logging.getLogger("eventflow.email")


# ---------------------------------------------------------------------------
# Public API — called by worker.py
# ---------------------------------------------------------------------------
def send_qr_email(
    recipient_email: str,
    recipient_name: str,
    registration_id: str,
    qr_image_path: str,
    event_name: str = "EventFlow Pro",
) -> None:
    """Send an email with the QR code image attached."""

    if not os.path.exists(qr_image_path):
        logger.error("QR image not found: %s", qr_image_path)
        raise FileNotFoundError(f"QR image not found: {qr_image_path}")

    # Route to the correct email backend
    if settings.RESEND_API_KEY:
        _send_via_resend(recipient_email, recipient_name, registration_id, qr_image_path, event_name)
    elif settings.SMTP_EMAIL and settings.SMTP_PASSWORD:
        _send_via_smtp(recipient_email, recipient_name, registration_id, qr_image_path, event_name)
    else:
        logger.error("No email backend configured. Set RESEND_API_KEY or SMTP_EMAIL/SMTP_PASSWORD.")
        raise ValueError("No email backend configured.")


# ---------------------------------------------------------------------------
# Resend (HTTP-based — works on Render, Railway, and all platforms)
# ---------------------------------------------------------------------------
def _send_via_resend(
    recipient_email: str,
    recipient_name: str,
    registration_id: str,
    qr_image_path: str,
    event_name: str,
) -> None:
    """Send email via Resend HTTP API."""
    import resend

    resend.api_key = settings.RESEND_API_KEY

    # Read QR image and base64-encode for attachment
    with open(qr_image_path, "rb") as f:
        qr_bytes = f.read()

    body_html = (
        f"<p>Hello {recipient_name},</p>"
        f"<p>Thank you for registering for <strong>{event_name}</strong>.</p>"
        f"<p>Your registration has been confirmed.</p>"
        f"<p>Your Registration ID: <strong>{registration_id}</strong></p>"
        f"<p>Please find your QR Code attached. Carry this QR Code on the event day.</p>"
        f"<p>Regards,<br>EventFlow Team</p>"
    )

    logger.info("  Sending email via Resend API to %s ...", recipient_email)

    params = {
        "from": settings.RESEND_FROM_EMAIL,
        "to": [recipient_email],
        "subject": f"{event_name} — Registration Confirmed",
        "html": body_html,
        "attachments": [
            {
                "filename": f"{registration_id}.png",
                "content": list(qr_bytes),
            }
        ],
    }

    response = resend.Emails.send(params)
    logger.info("  Email sent via Resend. ID: %s", response.get("id", "unknown"))


# ---------------------------------------------------------------------------
# SMTP (direct — works locally, blocked on Render free tier)
# ---------------------------------------------------------------------------
def _send_via_smtp(
    recipient_email: str,
    recipient_name: str,
    registration_id: str,
    qr_image_path: str,
    event_name: str,
) -> None:
    """Send email via direct SMTP connection (Gmail etc.)."""

    # --- Build the email ---
    msg = MIMEMultipart()
    msg["From"] = settings.SMTP_EMAIL
    msg["To"] = recipient_email
    msg["Subject"] = "Event Registration Successful"

    body = (
        f"Hello {recipient_name},\n\n"
        f"Thank you for registering.\n\n"
        f"Your registration has been confirmed.\n\n"
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

    # --- Send with step-by-step logging ---
    try:
        logger.info("  Connecting SMTP... (%s:%d)", settings.SMTP_HOST, settings.SMTP_PORT)
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=30) as server:
            server.starttls()
            logger.info("  TLS established")

            try:
                server.login(settings.SMTP_EMAIL, settings.SMTP_PASSWORD)
                logger.info("  SMTP Login Successful")
            except smtplib.SMTPAuthenticationError as e:
                logger.error("  SMTP Authentication Failed: %s", e)
                logger.error("    -> Verify SMTP_EMAIL and SMTP_PASSWORD in .env")
                logger.error("    -> Gmail requires a 16-char App Password, not your normal password")
                logger.error("    -> Generate at: https://myaccount.google.com/apppasswords")
                raise

            logger.info("  Sending Email to %s ...", recipient_email)
            server.send_message(msg)
            logger.info("  Email Sent via SMTP")

    except smtplib.SMTPAuthenticationError:
        raise  # Already logged above
    except smtplib.SMTPException as e:
        logger.error("  SMTP Error: %s", e)
        raise
    except OSError as e:
        logger.error("  Network Error (cannot reach SMTP server): %s", e)
        raise
