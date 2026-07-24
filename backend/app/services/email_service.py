"""
Email Service.
Sends emails with QR code attachments via SMTP.
"""

import os
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

from app.config import settings

logger = logging.getLogger("eventflow.email")


def send_qr_email(
    recipient_email: str,
    recipient_name: str,
    registration_id: str,
    qr_image_path: str,
    event_name: str = "EventFlow Pro",
) -> None:
    """Send an email with the QR code image attached."""

    # --- Pre-flight checks ---
    if not settings.SMTP_EMAIL or not settings.SMTP_PASSWORD:
        logger.error("✗ SMTP credentials missing in .env (SMTP_EMAIL or SMTP_PASSWORD is empty)")
        raise ValueError("SMTP_EMAIL and SMTP_PASSWORD must be set in .env")

    if not os.path.exists(qr_image_path):
        logger.error("✗ QR image not found: %s", qr_image_path)
        raise FileNotFoundError(f"QR image not found: {qr_image_path}")

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
        logger.info("  ✓ Connecting SMTP... (%s:%d)", settings.SMTP_HOST, settings.SMTP_PORT)
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=30) as server:
            server.starttls()
            logger.info("  ✓ TLS established")

            try:
                server.login(settings.SMTP_EMAIL, settings.SMTP_PASSWORD)
                logger.info("  ✓ SMTP Login Successful")
            except smtplib.SMTPAuthenticationError as e:
                logger.error("  ✗ SMTP Authentication Failed: %s", e)
                logger.error("    → Verify SMTP_EMAIL and SMTP_PASSWORD in .env")
                logger.error("    → Gmail requires a 16-char App Password, not your normal password")
                logger.error("    → Generate at: https://myaccount.google.com/apppasswords")
                raise

            logger.info("  ✓ Sending Email to %s ...", recipient_email)
            server.send_message(msg)
            logger.info("  ✓ Email Sent")

    except smtplib.SMTPAuthenticationError:
        raise  # Already logged above
    except smtplib.SMTPException as e:
        logger.error("  ✗ SMTP Error: %s", e)
        raise
    except OSError as e:
        logger.error("  ✗ Network Error (cannot reach SMTP server): %s", e)
        raise

