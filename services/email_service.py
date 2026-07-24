"""Email Service - Sends emails with QR code attachments via SMTP."""

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from dotenv import load_dotenv

load_dotenv()

# SMTP config from environment
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_EMAIL = os.getenv("SMTP_EMAIL", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")


class EmailService:
    """Sends emails with QR code image attachments."""

    def __init__(self):
        if not SMTP_EMAIL or not SMTP_PASSWORD:
            raise ValueError(
                "SMTP_EMAIL and SMTP_PASSWORD must be set in .env\n"
                "For Gmail, use an App Password (not your login password)."
            )
        self.smtp_host = SMTP_HOST
        self.smtp_port = SMTP_PORT
        self.sender_email = SMTP_EMAIL
        self.password = SMTP_PASSWORD

    def send_qr_email(self, recipient_email, recipient_name, registration_id, qr_image_path, event_name="EventFlow AI Conference"):
        """Send an email with the QR code attached."""
        if not os.path.exists(qr_image_path):
            raise FileNotFoundError(f"QR image not found: {qr_image_path}")

        # Build the email
        msg = MIMEMultipart()
        msg["From"] = self.sender_email
        msg["To"] = recipient_email
        msg["Subject"] = f"Your QR Code for {event_name} — {registration_id}"

        # Email body
        body = (
            f"Hi {recipient_name},\n\n"
            f"Thank you for registering for {event_name}!\n\n"
            f"Your Registration ID: {registration_id}\n\n"
            f"Please find your QR code attached. Show this at the event entrance for check-in.\n\n"
            f"See you there!\n"
            f"— {event_name} Team"
        )
        msg.attach(MIMEText(body, "plain"))

        # Attach QR image
        with open(qr_image_path, "rb") as f:
            qr_img = MIMEImage(f.read(), name=f"{registration_id}.png")
            qr_img.add_header("Content-Disposition", "attachment", filename=f"{registration_id}.png")
            msg.attach(qr_img)

        # Send
        try:
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.password)
                server.send_message(msg)
        except smtplib.SMTPAuthenticationError:
            raise ConnectionError(
                "SMTP authentication failed. Check SMTP_EMAIL and SMTP_PASSWORD.\n"
                "For Gmail, enable 2FA and create an App Password."
            )
        except Exception as e:
            raise ConnectionError(f"Failed to send email to {recipient_email}: {e}")
