"""
Email Service for MANTHAN | EventFlow Pro.
Ultra-resilient email delivery with automatic Dual-Port fallback (SSL 465 -> TLS 587)
and QR code attachments via Gmail SMTP.
"""

import os
import ssl
import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

from app.config import settings

logger = logging.getLogger("eventflow.email")


def _send_via_ssl_465(host: str, username: str, password: str, recipient: str, msg_str: str) -> None:
    """Attempt instant SSL delivery on port 465."""
    context = ssl.create_default_context()
    server = smtplib.SMTP_SSL(host, 465, context=context, timeout=10)
    server.login(username, password)
    server.sendmail(username, recipient, msg_str)
    server.quit()


def _send_via_tls_587(host: str, username: str, password: str, recipient: str, msg_str: str) -> None:
    """Attempt STARTTLS delivery on port 587."""
    server = smtplib.SMTP(host, 587, timeout=10)
    server.ehlo()
    context = ssl.create_default_context()
    server.starttls(context=context)
    server.ehlo()
    server.login(username, password)
    server.sendmail(username, recipient, msg_str)
    server.quit()


def _send_email(msg: MIMEMultipart) -> None:
    """
    Send email via SMTP with high resilience.
    Tries direct SSL (Port 465) first; if blocked by cloud firewall, falls back to STARTTLS (Port 587).
    """
    host = os.getenv("SMTP_HOST") or settings.SMTP_HOST or "smtp.gmail.com"
    username = os.getenv("SMTP_EMAIL") or settings.SMTP_EMAIL or "mradulg2122@gmail.com"
    raw_pwd = os.getenv("SMTP_PASSWORD") or settings.SMTP_PASSWORD or ""
    
    # Strip spaces and surrounding quotes if user copied 'xxxx xxxx xxxx xxxx'
    password = raw_pwd.replace(" ", "").replace('"', '').replace("'", "").strip()

    if not username:
        raise ValueError("SMTP_EMAIL is not set in environment!")
    if not password:
        raise ValueError("SMTP_PASSWORD is not set in environment! Please configure SMTP_PASSWORD in Render/backend .env.")

    recipient = msg["To"]
    msg_str = msg.as_string()

    logger.info("⚡ [SMTP] Attempting delivery to %s via %s (Sender: %s)...", recipient, host, username)

    # Method 1: Try Port 465 (Direct SSL)
    try:
        _send_via_ssl_465(host, username, password, recipient, msg_str)
        logger.info("✅ [SMTP] Dispatched instantly via Port 465 (SSL) to %s", recipient)
        return
    except Exception as err_465:
        logger.warning("⚠️ [SMTP] Port 465 failed (%s). Falling back to Port 587 (STARTTLS)...", err_465)

    # Method 2: Fallback to Port 587 (STARTTLS)
    try:
        _send_via_tls_587(host, username, password, recipient, msg_str)
        logger.info("✅ [SMTP] Dispatched successfully via Port 587 (STARTTLS) to %s", recipient)
        return
    except Exception as err_587:
        logger.error("❌ [SMTP] Both Port 465 and Port 587 failed for %s. Error: %s", recipient, err_587)
        raise RuntimeError(f"SMTP delivery failed on both ports: {err_587}")


def send_qr_email(
    recipient_email: str,
    recipient_name: str,
    registration_id: str,
    qr_image_path: str,
    event_name: str = "MANTHAN | The Freshers' Showdown",
) -> None:
    """Send registration confirmation email with QR pass attached instantly."""

    if not os.path.exists(qr_image_path):
        logger.error("QR image not found: %s", qr_image_path)
        raise FileNotFoundError(f"QR image not found: {qr_image_path}")

    sender_email = os.getenv("SMTP_EMAIL") or settings.SMTP_EMAIL or "mradulg2122@gmail.com"

    msg = MIMEMultipart("mixed")
    msg["From"] = f"MANTHAN — Saturangle Debate Club <{sender_email}>"
    msg["To"] = recipient_email
    msg["Subject"] = f"Registration Confirmed: MANTHAN | The Freshers' Showdown ({registration_id})"

    plain_body = f"""Hello {recipient_name},

Thank you for registering for MANTHAN | THE FRESHERS' SHOWDOWN (PRARAMBH 2K26), hosted by Saturangle – The Debate Club, GLA University.

Your Registration has been confirmed!

---
Registration ID: {registration_id}
Event: MANTHAN | The Freshers' Showdown
Date: 03 September 2026
Time: 01:00 PM – 03:00 PM
Venue: Arambh Hall AB-11 (CSED BLOCK)
---

Your official entry QR Code pass is attached to this email.
Please carry a digital or printed copy of your QR Code on the event day for instant check-in.

Event Coordinators:
- Mradul Gaur: +91 7417255432
- Nakshtra Chaudhary: +91 9258626362

Regards,
Saturangle Debate Club & EventFlow Pro
"""

    html_body = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    body {{ font-family: 'Segoe UI', Helvetica, Arial, sans-serif; background-color: #F7F4EC; margin: 0; padding: 20px; color: #102A43; }}
    .container {{ max-width: 600px; margin: 0 auto; background: #FFFFFF; border-radius: 12px; border: 1px solid #DDD7C9; overflow: hidden; box-shadow: 0 4px 12px rgba(16,42,67,0.08); }}
    .header {{ background: #102A43; color: #F7F4EC; padding: 28px 24px; text-align: center; border-bottom: 3px solid #C49A45; }}
    .badge {{ display: inline-block; background: rgba(196,154,69,0.2); border: 1px solid #C49A45; color: #ECD8A5; font-size: 11px; font-weight: bold; letter-spacing: 2px; text-transform: uppercase; padding: 4px 12px; border-radius: 20px; }}
    .title {{ font-size: 26px; font-weight: 800; margin: 10px 0 4px; letter-spacing: 1px; color: #FFFFFF; }}
    .subtitle {{ font-size: 13px; color: #C49A45; font-weight: 600; letter-spacing: 1px; text-transform: uppercase; }}
    .content {{ padding: 28px 24px; }}
    .card {{ background: #FAF8F3; border: 1px solid #DDD7C9; border-radius: 8px; padding: 18px; margin: 20px 0; }}
    .reg-id {{ font-size: 22px; font-family: monospace; font-weight: bold; color: #102A43; margin-top: 4px; }}
    .detail-row {{ margin: 6px 0; font-size: 14px; color: #334E68; }}
    .detail-row strong {{ color: #102A43; }}
    .qr-note {{ background: #F6EEDA; border-left: 4px solid #C49A45; padding: 12px; border-radius: 4px; font-size: 13px; color: #627D98; margin: 20px 0; }}
    .footer {{ background: #FAF8F3; padding: 20px 24px; text-align: center; border-top: 1px solid #DDD7C9; font-size: 12px; color: #627D98; }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <div class="badge">PRARAMBH 2K26</div>
      <div class="title">MANTHAN</div>
      <div class="subtitle">The Freshers' Showdown</div>
    </div>
    <div class="content">
      <p style="font-size: 16px; margin-top: 0;">Dear <strong>{recipient_name}</strong>,</p>
      <p style="font-size: 14px; line-height: 1.6; color: #334E68;">
        Congratulations! Your official registration for <strong>MANTHAN: The Freshers' Showdown</strong> has been successfully confirmed.
      </p>
      
      <div class="card">
        <div style="font-size: 11px; font-weight: bold; text-transform: uppercase; letter-spacing: 1px; color: #C49A45;">Official Registration Pass</div>
        <div class="reg-id">{registration_id}</div>
        <hr style="border: none; border-top: 1px solid #DDD7C9; margin: 12px 0;">
        <div class="detail-row"><strong>Event:</strong> MANTHAN (Round 1: Speech · Round 2: Debate)</div>
        <div class="detail-row"><strong>Date:</strong> 03 September 2026</div>
        <div class="detail-row"><strong>Time:</strong> 01:00 PM – 03:00 PM</div>
        <div class="detail-row"><strong>Venue:</strong> Arambh Hall AB-11 (CSED BLOCK)</div>
        <div class="detail-row"><strong>Club:</strong> Saturangle – The Debate Club</div>
      </div>

      <div class="qr-note">
        <strong>⚠️ Entry Pass:</strong> Your unique QR code is attached to this email (<code>{registration_id}.png</code>). Please carry it on your mobile device during check-in at the venue.
      </div>

      <p style="font-size: 13px; color: #627D98; margin-bottom: 0;">
        Need help? Contact student coordinators: <br>
        • <strong>Mradul Gaur:</strong> +91 7417255432 <br>
        • <strong>Nakshtra Chaudhary:</strong> +91 9258626362
      </p>
    </div>
    <div class="footer">
      © 2026 Saturangle Debate Club, GLA University · Powered by EventFlow Pro
    </div>
  </div>
</body>
</html>"""

    alt_part = MIMEMultipart("alternative")
    alt_part.attach(MIMEText(plain_body, "plain"))
    alt_part.attach(MIMEText(html_body, "html"))
    msg.attach(alt_part)

    # Attach QR image
    with open(qr_image_path, "rb") as f:
        qr_img = MIMEImage(f.read(), name=f"{registration_id}.png")
        qr_img.add_header(
            "Content-Disposition", "attachment",
            filename=f"{registration_id}.png",
        )
        msg.attach(qr_img)

    _send_email(msg)
