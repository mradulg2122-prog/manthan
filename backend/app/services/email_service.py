"""
Email Service.
Sends emails with QR code attachments via SMTP.

Uses Python's built-in smtplib + email modules.
"""

import os
import ssl
import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders

from app.config import settings

logger = logging.getLogger("eventflow.email")


def _send_email(msg: MIMEMultipart) -> None:
    """
    Send a MIMEMultipart email via SMTP.
    Reads SMTP settings from app.config.settings.

    Error handling:
      - authentication failure
      - connection failure
      - invalid recipient
      - TLS/SSL error
      - SMTP rejection
    """
    host = settings.SMTP_HOST
    port = settings.SMTP_PORT
    username = settings.SMTP_EMAIL
    password = settings.SMTP_PASSWORD

    if not host or not port:
        raise ValueError("SMTP_HOST and SMTP_PORT must be set in .env")
    if not username or not password:
        raise ValueError("SMTP_EMAIL and SMTP_PASSWORD must be set in .env")

    try:
        logger.info("  Connecting to SMTP server %s:%s ...", host, port)
        server = smtplib.SMTP(host, int(port), timeout=30)
        server.ehlo()

        # Start TLS for port 587 (STARTTLS)
        if int(port) == 587:
            context = ssl.create_default_context()
            server.starttls(context=context)
            server.ehlo()
            logger.info("  TLS connection established.")

        logger.info("  Authenticating as %s ...", username)
        server.login(username, password)

        sender = msg["From"]
        recipient = msg["To"]
        logger.info("  Sending email from %s to %s ...", sender, recipient)
        server.sendmail(sender, recipient, msg.as_string())

        server.quit()
        logger.info("  Email sent successfully via SMTP.")

    except smtplib.SMTPAuthenticationError as e:
        logger.error("  SMTP Authentication FAILED: %s", e)
        raise
    except smtplib.SMTPConnectError as e:
        logger.error("  SMTP Connection FAILED: %s", e)
        raise
    except smtplib.SMTPRecipientsRefused as e:
        logger.error("  SMTP Recipient REFUSED: %s", e)
        raise
    except ssl.SSLError as e:
        logger.error("  SMTP TLS/SSL Error: %s", e)
        raise
    except smtplib.SMTPException as e:
        logger.error("  SMTP Error: %s", e)
        raise
    except Exception as e:
        logger.error("  Email sending FAILED: %s", e)
        raise


def send_qr_email(
    recipient_email: str,
    recipient_name: str,
    registration_id: str,
    qr_image_path: str,
    event_name: str = "EventFlow Pro",
) -> None:
    """Send a registration confirmation email with QR code attached via SMTP."""

    # --- Pre-flight checks ---
    if not os.path.exists(qr_image_path):
        logger.error("QR image not found: %s", qr_image_path)
        raise FileNotFoundError(f"QR image not found: {qr_image_path}")

    sender_email = settings.SMTP_EMAIL

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

    # --- Send via SMTP ---
    _send_email(msg)


def send_certificate_email(
    recipient_email: str,
    recipient_name: str,
    registration_id: str,
    certificate_path: str,
    event_name: str = "EventFlow Pro",
) -> None:
    """Send a certificate email with PDF attached via SMTP."""

    # --- Pre-flight checks ---
    if not os.path.exists(certificate_path):
        logger.error("Certificate file not found: %s", certificate_path)
        raise FileNotFoundError(f"Certificate file not found: {certificate_path}")

    sender_email = settings.SMTP_EMAIL

    # --- Build the MIME email ---
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = f"{event_name} — Your Certificate"

    body = (
        f"Hello {recipient_name},\n\n"
        f"Thank you for participating in {event_name}.\n\n"
        f"Please find your certificate attached.\n\n"
        f"Your Registration ID: {registration_id}\n\n"
        f"Regards,\n"
        f"EventFlow Team"
    )
    msg.attach(MIMEText(body, "plain"))

    # --- Attach PDF certificate ---
    with open(certificate_path, "rb") as f:
        pdf_part = MIMEBase("application", "octet-stream")
        pdf_part.set_payload(f.read())
        encoders.encode_base64(pdf_part)
        filename = os.path.basename(certificate_path)
        pdf_part.add_header(
            "Content-Disposition", "attachment",
            filename=filename,
        )
        msg.attach(pdf_part)

    # --- Send via SMTP ---
    _send_email(msg)
