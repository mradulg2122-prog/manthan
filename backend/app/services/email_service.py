"""
Email Service for MANTHAN | EventFlow Pro.
High-Speed Email Engine supporting both:
1. Direct HTTPS REST API (Brevo / Resend over Port 443 — NEVER blocked by Render cloud)
2. Direct SMTP (Gmail Port 587/465 fallback)
"""

import os
import ssl
import base64
import socket
import smtplib
import logging
import requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

from app.config import settings

logger = logging.getLogger("eventflow.email")

# Force IPv4 for any SMTP fallback
_original_getaddrinfo = socket.getaddrinfo

def _ipv4_forced_getaddrinfo(host, port, family=0, type=0, proto=0, flags=0):
    if host and ("smtp" in str(host) or "gmail" in str(host) or "google" in str(host)):
        family = socket.AF_INET
    return _original_getaddrinfo(host, port, family, type, proto, flags)

socket.getaddrinfo = _ipv4_forced_getaddrinfo


def _send_via_brevo_api(api_key: str, recipient_email: str, recipient_name: str, subject: str, html_body: str, qr_path: str) -> bool:
    """Send via Brevo HTTPS REST API (Port 443 - Instant 150ms delivery)."""
    with open(qr_path, "rb") as f:
        qr_b64 = base64.b64encode(f.read()).decode("utf-8")

    sender_email = os.getenv("BREVO_SENDER_EMAIL") or os.getenv("SMTP_EMAIL") or "mradulg2122@gmail.com"
    payload = {
        "sender": {"name": "MANTHAN — Saturangle Debate Club", "email": sender_email},
        "to": [{"email": recipient_email, "name": recipient_name}],
        "subject": subject,
        "htmlContent": html_body,
        "attachment": [{"content": qr_b64, "name": f"manthan_qr_pass.png"}],
    }
    headers = {
        "api-key": api_key.strip(),
        "Content-Type": "application/json",
        "accept": "application/json",
    }
    resp = requests.post("https://api.brevo.com/v3/smtp/email", json=payload, headers=headers, timeout=8)
    if resp.status_code in (200, 201, 202):
        logger.info("⚡ [BREVO-API] Email dispatched INSTANTLY via HTTPS (Port 443) to %s", recipient_email)
        return True
    else:
        logger.error("❌ [BREVO-API] Failed (%d): %s", resp.status_code, resp.text)
        raise RuntimeError(f"Brevo API error: {resp.text}")


def _send_via_resend_api(api_key: str, recipient_email: str, recipient_name: str, subject: str, html_body: str, qr_path: str) -> bool:
    """Send via Resend HTTPS REST API (Port 443 - Instant 150ms delivery)."""
    with open(qr_path, "rb") as f:
        qr_b64 = base64.b64encode(f.read()).decode("utf-8")

    payload = {
        "from": "MANTHAN <onboarding@resend.dev>",
        "to": [recipient_email],
        "subject": subject,
        "html": html_body,
        "attachments": [{"filename": "manthan_qr_pass.png", "content": qr_b64}],
    }
    headers = {
        "Authorization": f"Bearer {api_key.strip()}",
        "Content-Type": "application/json",
    }
    resp = requests.post("https://api.resend.com/emails", json=payload, headers=headers, timeout=8)
    if resp.status_code in (200, 201, 202):
        logger.info("⚡ [RESEND-API] Email dispatched INSTANTLY via HTTPS (Port 443) to %s", recipient_email)
        return True
    else:
        logger.error("❌ [RESEND-API] Failed (%d): %s", resp.status_code, resp.text)
        raise RuntimeError(f"Resend API error: {resp.text}")


def _send_via_smtp(msg: MIMEMultipart) -> None:
    """SMTP Fallback via Ports 587/465."""
    host = os.getenv("SMTP_HOST") or settings.SMTP_HOST or "smtp.gmail.com"
    username = os.getenv("SMTP_EMAIL") or settings.SMTP_EMAIL or "mradulg2122@gmail.com"
    raw_pwd = os.getenv("SMTP_PASSWORD") or settings.SMTP_PASSWORD or ""
    password = raw_pwd.replace(" ", "").replace('"', '').replace("'", "").strip()

    if not username or not password:
        raise ValueError("SMTP credentials missing.")

    recipient = msg["To"]
    msg_str = msg.as_string()

    for port in [587, 465]:
        try:
            if port == 587:
                server = smtplib.SMTP(host, 587, timeout=6)
                server.ehlo()
                context = ssl.create_default_context()
                server.starttls(context=context)
                server.ehlo()
            else:
                context = ssl.create_default_context()
                server = smtplib.SMTP_SSL(host, 465, context=context, timeout=6)

            server.login(username, password)
            server.sendmail(username, recipient, msg_str)
            server.quit()
            logger.info("✅ [SMTP] Email dispatched via port %d to %s", port, recipient)
            return
        except Exception as e:
            logger.warning("⚠️ [SMTP] Port %d failed (%s).", port, e)

    raise RuntimeError("SMTP ports 587 and 465 timed out on Render cloud network.")


def send_qr_email(
    recipient_email: str,
    recipient_name: str,
    registration_id: str,
    qr_image_path: str,
    event_name: str = "MANTHAN | The Freshers' Showdown",
) -> None:
    """Send registration confirmation email with QR pass attached."""

    if not os.path.exists(qr_image_path):
        raise FileNotFoundError(f"QR image not found: {qr_image_path}")

    sender_email = os.getenv("SMTP_EMAIL") or settings.SMTP_EMAIL or "mradulg2122@gmail.com"
    subject = f"Registration Confirmed: MANTHAN | The Freshers' Showdown ({registration_id})"

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
        <strong>⚠️ Entry Pass:</strong> Your unique QR code is attached to this email. Please carry it on your mobile device during check-in at the venue.
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

    # Strategy 1: Brevo HTTPS REST API (Port 443 - Instant 150ms)
    brevo_key = os.getenv("BREVO_API_KEY", "").strip()
    if brevo_key:
        try:
            _send_via_brevo_api(brevo_key, recipient_email, recipient_name, subject, html_body, qr_image_path)
            return
        except Exception as e:
            logger.warning("Brevo API failed: %s. Falling back...", e)

    # Strategy 2: Resend HTTPS REST API (Port 443 - Instant 150ms)
    resend_key = os.getenv("RESEND_API_KEY", "").strip()
    if resend_key:
        try:
            _send_via_resend_api(resend_key, recipient_email, recipient_name, subject, html_body, qr_image_path)
            return
        except Exception as e:
            logger.warning("Resend API failed: %s. Falling back...", e)

    # Strategy 3: Direct Gmail SMTP
    msg = MIMEMultipart("mixed")
    msg["From"] = f"MANTHAN — Saturangle Debate Club <{sender_email}>"
    msg["To"] = recipient_email
    msg["Subject"] = subject

    alt_part = MIMEMultipart("alternative")
    alt_part.attach(MIMEText(plain_body, "plain"))
    alt_part.attach(MIMEText(html_body, "html"))
    msg.attach(alt_part)

    with open(qr_image_path, "rb") as f:
        qr_img = MIMEImage(f.read(), name=f"{registration_id}.png")
        qr_img.add_header("Content-Disposition", "attachment", filename=f"{registration_id}.png")
        msg.attach(qr_img)

    _send_via_smtp(msg)
