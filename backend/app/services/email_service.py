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
    brevo_key = (
        os.getenv("BREVO_API_KEY")
        or os.getenv("BREVO_KEY")
        or os.getenv("SENDINBLUE_API_KEY")
        or os.getenv("BREVO_TOKEN")
        or ""
    ).strip()

    if brevo_key:
        try:
            logger.info("🔑 [EmailEngine] Found Brevo API key (%s...) — dispatching via HTTPS Port 443...", brevo_key[:8])
            _send_via_brevo_api(brevo_key, recipient_email, recipient_name, subject, html_body, qr_image_path)
            return
        except Exception as e:
            logger.error("❌ Brevo API failed: %s. Falling back to SMTP...", e)
    else:
        logger.warning("⚠️ [EmailEngine] BREVO_API_KEY not found in environment. Falling back to SMTP.")

    # Strategy 2: Resend HTTPS REST API (Port 443 - Instant 150ms)
    resend_key = (
        os.getenv("RESEND_API_KEY")
        or os.getenv("RESEND_KEY")
        or os.getenv("RESEND_TOKEN")
        or ""
    ).strip()

    if resend_key:
        try:
            logger.info("🔑 [EmailEngine] Found Resend API key — dispatching via HTTPS Port 443...")
            _send_via_resend_api(resend_key, recipient_email, recipient_name, subject, html_body, qr_image_path)
            return
        except Exception as e:
            logger.error("❌ Resend API failed: %s. Falling back to SMTP...", e)

    # Strategy 3: Direct Gmail SMTP
    logger.info("⚡ [EmailEngine] Attempting direct Gmail SMTP for %s ...", recipient_email)
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


def send_thankyou_email(
    recipient_email: str,
    recipient_name: str,
    qr_image_path: str = None,
) -> None:
    """Send post-event appreciation and Saturangle Club recruitment email with QR code."""
    if qr_image_path is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        qr_image_path = os.path.join(base_dir, "assets", "saturangle_recruitment_qr.jpg")

    if not os.path.exists(qr_image_path):
        raise FileNotFoundError(f"Recruitment QR image not found: {qr_image_path}")

    with open(qr_image_path, "rb") as f:
        qr_bytes = f.read()
        qr_b64 = base64.b64encode(qr_bytes).decode("utf-8")

    sender_email = os.getenv("SMTP_EMAIL") or settings.SMTP_EMAIL or "mradulg2122@gmail.com"
    subject = "Thank You for Powering MANTHAN 2026! 🎙️ + Join Saturangle Debate Club"

    plain_body = f"""Dear {recipient_name},

Thank you for being an active part of MANTHAN: The Freshers' Showdown (Prarambh 2K26), organized by Saturangle – The Debate Club, GLA University!

Stepping up onto the stage, speaking your mind with conviction, and defending your arguments takes genuine courage. We were truly inspired by your enthusiasm, thought-provoking perspectives, and the vibrant energy you brought to the floor.

Whether this was your very first time debating or another milestone in your public speaking journey, we hope MANTHAN gave you valuable experience, boosted your confidence, and connected you with fellow passionate thinkers.

==================================================
🚀 WANT TO BE PART OF ORGANIZING SUCH FLAGSHIP EVENTS?
==================================================
If you loved the adrenaline of MANTHAN and want to lead, design, manage, or host upcoming university-level debates, conferences, and mega-events — WE ARE HIRING!

Saturangle – The Debate Club is officially recruiting for the upcoming academic tenure!

Open Domains:
• Debating & Public Speaking
• Event Planning & Stage Management
• Tech, Web & Operations
• Public Relations & Social Media Marketing
• Graphic Design & Media Production

📲 HOW TO JOIN:
Scan the attached Saturangle Recruitment QR Code to submit your application form.

Let’s turn ideas into impact, together!

Warm regards,
Team Saturangle – The Debate Club
GLA University, Mathura
Coordinators:
• Mradul Gaur: +91 7417255432
• Nakshtra Chaudhary: +91 9258626362
"""

    html_body = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Thank You for Participating in MANTHAN</title>
  <style>
    body {{ font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif; background-color: #F7F4EC; margin: 0; padding: 20px; color: #102A43; }}
    .container {{ max-width: 600px; margin: 0 auto; background: #FFFFFF; border-radius: 14px; border: 1px solid #DDD7C9; overflow: hidden; box-shadow: 0 6px 18px rgba(16,42,67,0.08); }}
    .header {{ background: linear-gradient(135deg, #102A43 0%, #1E3A5F 100%); color: #F7F4EC; padding: 32px 24px; text-align: center; border-bottom: 3px solid #C49A45; }}
    .badge {{ display: inline-block; background: rgba(196,154,69,0.25); border: 1px solid #C49A45; color: #ECD8A5; font-size: 11px; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; padding: 5px 14px; border-radius: 20px; margin-bottom: 8px; }}
    .title {{ font-size: 26px; font-weight: 800; margin: 6px 0 4px; color: #FFFFFF; letter-spacing: 0.5px; }}
    .subtitle {{ font-size: 13px; color: #C49A45; font-weight: 600; letter-spacing: 1.5px; text-transform: uppercase; }}
    .content {{ padding: 30px 26px; }}
    .quote-box {{ background: #FAF8F3; border-left: 4px solid #C49A45; border-radius: 0 8px 8px 0; padding: 14px 18px; margin: 20px 0; font-style: italic; color: #334E68; font-size: 14px; line-height: 1.6; }}
    .highlight-card {{ background: linear-gradient(145deg, #FAF8F3 0%, #F4EFE6 100%); border: 1px solid #E2D9C8; border-radius: 12px; padding: 22px; margin: 24px 0; text-align: center; }}
    .hiring-badge {{ display: inline-block; background: #E53E3E; color: #FFFFFF; font-size: 11px; font-weight: 800; letter-spacing: 1.5px; padding: 4px 12px; border-radius: 16px; text-transform: uppercase; margin-bottom: 10px; }}
    .hiring-title {{ font-size: 20px; font-weight: 800; color: #102A43; margin: 0 0 8px; }}
    .hiring-desc {{ font-size: 13px; color: #486581; line-height: 1.5; margin-bottom: 16px; }}
    .qr-container {{ background: #FFFFFF; border: 2px dashed #C49A45; border-radius: 12px; padding: 16px; display: inline-block; margin: 10px auto; }}
    .qr-img {{ width: 220px; height: 220px; display: block; border-radius: 8px; margin: 0 auto; }}
    .qr-instruction {{ font-size: 13px; font-weight: 700; color: #102A43; margin-top: 10px; }}
    .domain-tag {{ display: inline-block; background: #FFFFFF; border: 1px solid #DDD7C9; color: #102A43; font-size: 11px; font-weight: 600; padding: 4px 10px; border-radius: 12px; margin: 3px 2px; }}
    .footer {{ background: #FAF8F3; padding: 22px 24px; text-align: center; border-top: 1px solid #DDD7C9; font-size: 12px; color: #627D98; line-height: 1.6; }}
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
        On behalf of the entire team at <strong>Saturangle – The Debate Club</strong>, we want to extend our heartfelt gratitude to you for participating in <strong>MANTHAN: The Freshers' Showdown</strong>!
      </p>

      <div class="quote-box">
        "Debate is not just about having the last word; it is about building the courage to speak, the clarity to listen, and the wisdom to understand diverse perspectives."
      </div>

      <p style="font-size: 14px; line-height: 1.6; color: #334E68;">
        Taking the stage, articulating bold viewpoints, and engaging in intellectual combat takes immense dedication. Your enthusiasm, critical thinking, and articulate delivery made MANTHAN a tremendous success. We hope this experience gave you newfound confidence, lasting memories, and meaningful learnings!
      </p>

      <div class="highlight-card">
        <div class="hiring-badge">HIRING ALERT 🚀</div>
        <div class="hiring-title">Become a Part of Saturangle!</div>
        <div class="hiring-desc">
          Loved the energy of MANTHAN? Want to organize such mega events, lead debates, and develop leadership skills? <strong>Saturangle Club Recruitment is now officially OPEN!</strong>
        </div>

        <div class="qr-container">
          <img class="qr-img" src="cid:saturangle_recruitment_qr" alt="Scan to Join Saturangle">
        </div>
        <div class="qr-instruction">📲 Scan this QR Code to apply & join our club!</div>

        <div style="margin-top: 16px;">
          <span class="domain-tag">🎙️ Public Speaking</span>
          <span class="domain-tag">🎪 Event Management</span>
          <span class="domain-tag">💻 Tech & Operations</span>
          <span class="domain-tag">📢 PR & Marketing</span>
          <span class="domain-tag">🎨 Graphic Design</span>
        </div>
      </div>

      <p style="font-size: 13px; color: #627D98; margin-bottom: 0;">
        For queries or coordination:<br>
        • <strong>Mradul Gaur:</strong> +91 7417255432<br>
        • <strong>Nakshtra Chaudhary:</strong> +91 9258626362
      </p>
    </div>

    <div class="footer">
      <strong>Saturangle – The Debate Club</strong><br>
      GLA University, Mathura · Powered by EventFlow Pro<br>
      <em>"Empowering Voices, Shaping Perspectives"</em>
    </div>
  </div>
</body>
</html>"""

    # Strategy 1: Brevo HTTPS REST API
    brevo_key = (
        os.getenv("BREVO_API_KEY")
        or os.getenv("BREVO_KEY")
        or os.getenv("SENDINBLUE_API_KEY")
        or os.getenv("BREVO_TOKEN")
        or ""
    ).strip()

    if brevo_key:
        try:
            logger.info("🔑 [EmailEngine] Sending Thank You email via Brevo HTTPS API...")
            # For Brevo, embed image as attachment with cid reference or b64
            payload = {
                "sender": {"name": "MANTHAN — Saturangle Debate Club", "email": sender_email},
                "to": [{"email": recipient_email, "name": recipient_name}],
                "subject": subject,
                "htmlContent": html_body.replace("cid:saturangle_recruitment_qr", f"data:image/jpeg;base64,{qr_b64}"),
                "attachment": [{"content": qr_b64, "name": "saturangle_recruitment_qr.jpg"}],
            }
            headers = {
                "api-key": brevo_key,
                "Content-Type": "application/json",
                "accept": "application/json",
            }
            resp = requests.post("https://api.brevo.com/v3/smtp/email", json=payload, headers=headers, timeout=8)
            if resp.status_code in (200, 201, 202):
                logger.info("⚡ [BREVO-API] Thank You email dispatched to %s", recipient_email)
                return
        except Exception as e:
            logger.error("❌ Brevo API failed for Thank You email: %s. Falling back to SMTP...", e)

    # Strategy 2: Direct Gmail SMTP
    logger.info("⚡ [EmailEngine] Dispatching Thank You email via direct SMTP to %s ...", recipient_email)
    msg = MIMEMultipart("related")
    msg["From"] = f"MANTHAN — Saturangle Debate Club <{sender_email}>"
    msg["To"] = recipient_email
    msg["Subject"] = subject

    alt_part = MIMEMultipart("alternative")
    alt_part.attach(MIMEText(plain_body, "plain"))
    alt_part.attach(MIMEText(html_body, "html"))
    msg.attach(alt_part)

    qr_img = MIMEImage(qr_bytes, _subtype="jpeg")
    qr_img.add_header("Content-ID", "<saturangle_recruitment_qr>")
    qr_img.add_header("Content-Disposition", "inline", filename="saturangle_recruitment_qr.jpg")
    msg.attach(qr_img)

    _send_via_smtp(msg)


