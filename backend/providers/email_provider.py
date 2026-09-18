import os
import json
import logging
import smtplib
import time
import base64
import urllib.request
import urllib.error
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from typing import Dict, Any, Optional, List
from pathlib import Path
from backend.config import settings, BASE_DIR

logger = logging.getLogger("ZavranAI.EmailProvider")

_LOGO_BASE64_CACHE: Optional[str] = None

def get_logo_base64() -> str:
    """Reads and caches the base64 data of zevaro.png for email embedding."""
    global _LOGO_BASE64_CACHE
    if _LOGO_BASE64_CACHE is not None:
        return _LOGO_BASE64_CACHE
    
    logo_path = getattr(settings, "ZAVRAN_LOGO_PATH", None) or (BASE_DIR / "zevaro.png")
    if logo_path and os.path.exists(logo_path):
        try:
            with open(logo_path, "rb") as f:
                _LOGO_BASE64_CACHE = base64.b64encode(f.read()).decode("utf-8")
                return _LOGO_BASE64_CACHE
        except Exception as e:
            logger.warning(f"Could not load zevaro.png logo: {e}")
    return ""


def get_default_from_email() -> str:
    return settings.SMTP_FROM_EMAIL or "support.zarvanai@gmail.com"


class BaseEmailProvider:
    """Abstract interface for transactional email delivery."""
    async def send_email(
        self,
        to_email: str,
        subject: str,
        html_body: str,
        text_body: str,
        from_email: Optional[str] = None,
    ) -> Dict[str, Any]:
        raise NotImplementedError


class ResendEmailProvider(BaseEmailProvider):
    """Resend REST API Email Delivery Provider."""
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.RESEND_API_KEY
        self.endpoint = "https://api.resend.com/emails"

    async def send_email(
        self,
        to_email: str,
        subject: str,
        html_body: str,
        text_body: str,
        from_email: Optional[str] = None,
    ) -> Dict[str, Any]:
        if not self.api_key:
            raise ValueError("RESEND_API_KEY is not configured.")

        sender = from_email or get_default_from_email()
        
        # Resend test API allows 'onboarding@resend.dev' or any verified custom domain
        if "@gmail.com" in sender.lower() or "zarvanai" in sender.lower():
            send_from = "Zavran AI <onboarding@resend.dev>"
            reply_to = sender
        else:
            send_from = f"Zavran AI <{sender}>" if "<" not in sender else sender
            reply_to = sender

        payload = {
            "from": send_from,
            "to": [to_email],
            "reply_to": reply_to,
            "subject": subject,
            "html": html_body,
            "text": text_body,
        }
        data_bytes = json.dumps(payload).encode("utf-8")
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "ZavranAI-Backend/1.0",
        }
        req = urllib.request.Request(self.endpoint, data=data_bytes, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req) as resp:
                res_data = json.loads(resp.read().decode("utf-8"))
                return {"success": True, "provider": "resend", "id": res_data.get("id")}
        except urllib.error.HTTPError as e:
            err_msg = e.read().decode("utf-8")
            logger.error(f"Resend HTTP error ({e.code}): {err_msg}")
            raise RuntimeError(f"Resend API error: {e.code} - {err_msg}")


class SendGridEmailProvider(BaseEmailProvider):
    """SendGrid v3 Mail Send API Provider."""
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.SENDGRID_API_KEY
        self.endpoint = "https://api.sendgrid.com/v3/mail/send"

    async def send_email(
        self,
        to_email: str,
        subject: str,
        html_body: str,
        text_body: str,
        from_email: Optional[str] = None,
    ) -> Dict[str, Any]:
        if not self.api_key:
            raise ValueError("SENDGRID_API_KEY is not configured.")

        sender = from_email or get_default_from_email()
        clean_email = sender.split("<")[-1].replace(">", "").strip() if "<" in sender else sender

        payload = {
            "personalizations": [{"to": [{"email": to_email}]}],
            "from": {"email": clean_email, "name": "Zavran AI"},
            "subject": subject,
            "content": [
                {"type": "text/plain", "value": text_body},
                {"type": "text/html", "value": html_body},
            ],
        }
        data_bytes = json.dumps(payload).encode("utf-8")
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "ZavranAI-Backend/1.0",
        }
        req = urllib.request.Request(self.endpoint, data=data_bytes, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req) as resp:
                return {"success": True, "provider": "sendgrid", "status_code": resp.status}
        except urllib.error.HTTPError as e:
            err_msg = e.read().decode("utf-8")
            logger.error(f"SendGrid HTTP error ({e.code}): {err_msg}")
            raise RuntimeError(f"SendGrid API error: {e.code} - {err_msg}")


class SMTPEmailProvider(BaseEmailProvider):
    """Standard SMTP TLS/SSL Email Delivery Provider."""
    def __init__(self):
        self.host = settings.SMTP_HOST
        self.port = settings.SMTP_PORT
        self.user = settings.SMTP_USER
        self.password = settings.SMTP_PASSWORD
        self.from_email = get_default_from_email()

    async def send_email(
        self,
        to_email: str,
        subject: str,
        html_body: str,
        text_body: str,
        from_email: Optional[str] = None,
    ) -> Dict[str, Any]:
        if not self.host:
            raise ValueError("SMTP_HOST is not configured.")

        sender = from_email or self.from_email
        clean_sender = sender.split("<")[-1].replace(">", "").strip() if "<" in sender else sender

        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"Zavran AI <{clean_sender}>"
        msg["To"] = to_email

        msg.attach(MIMEText(text_body, "plain", "utf-8"))
        msg.attach(MIMEText(html_body, "html", "utf-8"))

        logo_path = getattr(settings, "ZAVRAN_LOGO_PATH", None) or (BASE_DIR / "zevaro.png")
        if logo_path and os.path.exists(logo_path):
            try:
                with open(logo_path, "rb") as f:
                    img_data = f.read()
                    img = MIMEImage(img_data, name="zevaro.png")
                    img.add_header("Content-ID", "<zavran_logo>")
                    img.add_header("Content-Disposition", "inline", filename="zevaro.png")
                    msg.attach(img)
            except Exception as e:
                logger.warning(f"Could not attach zevaro.png to SMTP email: {e}")

        try:
            with smtplib.SMTP(self.host, self.port) as server:
                server.starttls()
                if self.user and self.password:
                    server.login(self.user, self.password)
                server.sendmail(clean_sender, [to_email], msg.as_string())
            return {"success": True, "provider": "smtp"}
        except Exception as e:
            logger.error(f"SMTP error sending email to {to_email}: {e}")
            raise RuntimeError(f"SMTP error: {str(e)}")


class MockConsoleEmailProvider(BaseEmailProvider):
    """Safe local development fallback that records and logs dispatched emails."""
    def __init__(self):
        self.sent_emails: List[Dict[str, Any]] = []

    async def send_email(
        self,
        to_email: str,
        subject: str,
        html_body: str,
        text_body: str,
        from_email: Optional[str] = None,
    ) -> Dict[str, Any]:
        sender = from_email or get_default_from_email()
        record = {
            "to": to_email,
            "from": sender,
            "subject": subject,
            "text": text_body,
            "html": html_body,
            "timestamp": time.time(),
        }
        self.sent_emails.append(record)
        logger.info(f"[MockConsoleEmailProvider] Dispatched email from '{sender}' to '{to_email}' with subject '{subject}'.")
        return {"success": True, "provider": "mock_console", "to": to_email, "from": sender, "subject": subject}


def _render_email_brand_header(subtitle: str = "Precision AI Technical Assessment") -> str:
    logo_b64 = get_logo_base64()
    logo_img_src = f"data:image/png;base64,{logo_b64}" if logo_b64 else "zevaro.png"
    return f"""
    <div style="background: #020617; padding: 28px 28px; border-bottom: 1px solid #1e293b;">
      <table cellpadding="0" cellspacing="0" border="0" style="width: 100%;">
        <tr>
          <td style="vertical-align: middle; width: 48px;">
            <img src="{logo_img_src}" alt="Zavran AI Logo" width="44" height="44" style="display: block; border-radius: 10px; border: 1px solid rgba(255,255,255,0.15); background: #ffffff; padding: 2px;" />
          </td>
          <td style="vertical-align: middle; padding-left: 14px;">
            <div style="font-size: 20px; font-weight: 800; color: #ffffff; letter-spacing: -0.5px; line-height: 1.2;">Zavran AI</div>
            <div style="font-size: 11px; color: #94a3b8; font-family: monospace; text-transform: uppercase; letter-spacing: 0.5px; margin-top: 3px;">{subtitle}</div>
          </td>
        </tr>
      </table>
    </div>
    """

def _render_email_footer() -> str:
    return """
    <div style="background: #f8fafc; padding: 22px 28px; font-size: 12px; color: #64748b; border-top: 1px solid #e2e8f0; text-align: center;">
      <p style="margin: 0; font-weight: 600; color: #334155;">&copy; 2026 Zavran AI Inc. All rights reserved.</p>
      <p style="margin: 4px 0 0; font-size: 11px; color: #94a3b8;">
        Official Inquiries: <a href="mailto:support.zarvanai@gmail.com" style="color: #4f46e5; text-decoration: none;">support.zarvanai@gmail.com</a>
      </p>
      <p style="margin: 4px 0 0; font-size: 11px; color: #94a3b8;">
        Zero-Trust Proctoring &bull; Multi-Agent Rigor Calibration &bull; SOC-2 & ISO-27001 Compliant
      </p>
    </div>
    """


class EmailService:
    """
    High-level Transactional Email Service for Zavran AI.
    Handles all 5 core communication triggers:
      1. Welcome / Greeting Email (on user signup/login)
      2. Interview Scheduled Email (with full session details)
      3. Interview Room Ready Email (room link and access code)
      4. Interview Completed Email (submission confirmation & 10-min report notice)
      5. Interview Review & Feedback Report Email (detailed score, strengths, taxonomy)
    """
    _provider: Optional[BaseEmailProvider] = None
    dispatched_history: List[Dict[str, Any]] = []

    @classmethod
    def get_provider(cls) -> BaseEmailProvider:
        if cls._provider is not None:
            return cls._provider

        if settings.RESEND_API_KEY:
            cls._provider = ResendEmailProvider()
        elif settings.SENDGRID_API_KEY:
            cls._provider = SendGridEmailProvider()
        elif settings.SMTP_HOST:
            cls._provider = SMTPEmailProvider()
        else:
            cls._provider = MockConsoleEmailProvider()

        return cls._provider

    @classmethod
    def set_provider(cls, provider: BaseEmailProvider):
        """Allows test mocking."""
        cls._provider = provider

    # -------------------------------------------------------------------------
    # 1. WELCOME / GREETING EMAIL (On Signup / Newly Entered)
    # -------------------------------------------------------------------------
    @classmethod
    def generate_welcome_email_content(
        cls,
        candidate_name: str,
        email: str,
        base_url: Optional[str] = None,
    ) -> Dict[str, str]:
        app_url = base_url or settings.APP_BASE_URL or "http://localhost:8000"
        portal_url = f"{app_url}/candidate-portal.html#profile"
        subject = "Welcome to Zavran AI — Precision Technical Interview Preparation"

        text_body = f"""Hi {candidate_name},

Welcome to Zavran AI!

Your candidate account ({email}) is now active. Zavran AI provides precision, evidence-based technical interview simulations calibrated against Staff & FAANG rubrics.

What you can do next:
1. Upload & Calibrate Your Resume: Parse your background into granular technical competencies.
2. Select From 200+ Roles: Tailor scenarios from Distributed Systems Architect to AI/ML Engineer.
3. Live AI Evaluators: Practice with our voice agents (Zaroon, Aarin, Soni) with zero-leak proctoring.
4. Comprehensive Feedback: Receive concept-level depth taxonomy analysis and actionable study focus areas within minutes.

Get Started & Access Your Candidate Portal:
{portal_url}

If you have any questions or need support, contact our team directly at support.zarvanai@gmail.com.

Best regards,
The Zavran AI Team
support.zarvanai@gmail.com
"""

        brand_header = _render_email_brand_header(subtitle="Candidate Onboarding • Welcome")
        footer = _render_email_footer()

        html_body = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>{subject}</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #0f172a; margin: 0; padding: 24px; color: #1e293b; }}
    .container {{ max-width: 600px; margin: 0 auto; background: #ffffff; border-radius: 20px; overflow: hidden; box-shadow: 0 10px 25px rgba(0,0,0,0.12); border: 1px solid #e2e8f0; }}
    .content {{ padding: 28px; font-size: 14px; line-height: 1.6; color: #334155; }}
    .feature-card {{ background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 14px; padding: 16px 18px; margin: 12px 0; }}
    .feature-title {{ font-size: 13px; font-weight: 700; color: #0f172a; margin-bottom: 4px; }}
    .cta-container {{ text-align: center; margin: 28px 0; }}
    .cta-button {{ display: inline-block; background: #020617; color: #ffffff !important; text-decoration: none; padding: 14px 32px; border-radius: 12px; font-weight: bold; font-size: 14px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); }}
  </style>
</head>
<body>
  <div class="container">
    {brand_header}
    <div class="content">
      <p style="font-size: 16px; font-weight: 600; color: #0f172a; margin-top: 0;">Hi <strong>{candidate_name}</strong>,</p>
      <p>Welcome to <strong>Zavran AI</strong>! We are excited to support your technical interview journey with high-rigor, simulated AI evaluations.</p>
      
      <p>Here is what makes Zavran AI your unfair advantage:</p>

      <div class="feature-card">
        <div class="feature-title">🎯 Staff &amp; FAANG Calibrated Rubrics</div>
        <div style="font-size: 12px; color: #64748b;">Practice across 200+ specialized roles with adaptive systems design, concurrency, and architecture questions.</div>
      </div>

      <div class="feature-card">
        <div class="feature-title">🎙️ Real-Time Voice Evaluators</div>
        <div style="font-size: 12px; color: #64748b;">Engage with specialized interview personas including <strong>Zaroon</strong> (High-Rigor Architecture), <strong>Aarin</strong>, and <strong>Soni</strong>.</div>
      </div>

      <div class="feature-card">
        <div class="feature-title">📊 10-Minute Deep Technical Reports</div>
        <div style="font-size: 12px; color: #64748b;">Receive evidence-backed scoring, depth taxonomy levels (Level 1–5), concept coverage, and prioritized improvement areas.</div>
      </div>

      <div class="cta-container">
        <a href="{portal_url}" class="cta-button">Enter Candidate Portal &rarr;</a>
      </div>

      <p style="font-size: 12px; color: #64748b; text-align: center;">
        Direct link: <a href="{portal_url}" style="color: #4f46e5;">{portal_url}</a>
      </p>
    </div>
    {footer}
  </div>
</body>
</html>
"""
        return {"subject": subject, "text": text_body, "html": html_body, "url": portal_url}

    @classmethod
    async def send_welcome_email(
        cls,
        to_email: str,
        candidate_name: str,
        base_url: Optional[str] = None,
    ) -> Dict[str, Any]:
        if not to_email or "@" not in to_email:
            raise ValueError(f"Invalid recipient email address: '{to_email}'")

        content = cls.generate_welcome_email_content(
            candidate_name=candidate_name,
            email=to_email,
            base_url=base_url,
        )
        provider = cls.get_provider()
        res = await provider.send_email(
            to_email=to_email,
            subject=content["subject"],
            html_body=content["html"],
            text_body=content["text"],
        )
        dispatch_log = {
            "type": "WELCOME_GREETINGS",
            "to_email": to_email,
            "candidate_name": candidate_name,
            "timestamp": time.time(),
            "status": "SENT",
            "provider_response": res,
        }
        cls.dispatched_history.append(dispatch_log)
        logger.info(f"Welcome email successfully sent from {get_default_from_email()} to {to_email}")
        return res

    # -------------------------------------------------------------------------
    # 2. INTERVIEW SCHEDULED EMAIL (With All Details)
    # -------------------------------------------------------------------------
    @classmethod
    def generate_scheduled_email_content(
        cls,
        candidate_name: str,
        room_code: str,
        role: str,
        company: str,
        interviewer_name: str,
        interview_date: str,
        interview_time: str,
        base_url: Optional[str] = None,
    ) -> Dict[str, str]:
        app_url = base_url or settings.APP_BASE_URL or "http://localhost:8000"
        history_url = f"{app_url}/candidate-portal.html#history"
        subject = f"Interview Scheduled — {role} at {company or 'Zavran AI Partner'} (Zavran AI)"

        text_body = f"""ZAVRAN AI — INTERVIEW CONFIRMATION

Dear {candidate_name},

Your AI technical interview has been successfully scheduled.

============================================================
SESSION DETAILS
============================================================
Company / Org:  {company or 'Zavran AI Partner'}
Target Role:    {role}
AI Evaluator:   {interviewer_name} (AI Technical Evaluator)
Date:           {interview_date}
Time Slot:      {interview_time} (30 minutes)
Room Code:      {room_code}
============================================================

Preparation Checklist:
- Ensure a stable internet connection and quiet room.
- Test your microphone and camera permissions beforehand.
- Join the room 2-3 minutes before your scheduled start time.
- When the room becomes ready, you will receive a notification and direct access link.

View Your Scheduled Session in Candidate Portal:
{history_url}

Need support? Contact support.zarvanai@gmail.com.

Best regards,
Zavran AI Evaluation Team
support.zarvanai@gmail.com
"""

        brand_header = _render_email_brand_header(subtitle="Interview Scheduled • Confirmation")
        footer = _render_email_footer()

        html_body = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>{subject}</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #0f172a; margin: 0; padding: 24px; color: #1e293b; }}
    .container {{ max-width: 600px; margin: 0 auto; background: #ffffff; border-radius: 20px; overflow: hidden; box-shadow: 0 10px 25px rgba(0,0,0,0.12); border: 1px solid #e2e8f0; }}
    .content {{ padding: 28px; font-size: 14px; line-height: 1.6; color: #334155; }}
    .table-container {{ margin: 20px 0; border: 1px solid #e2e8f0; border-radius: 14px; overflow: hidden; background: #f8fafc; }}
    .details-table {{ width: 100%; border-collapse: collapse; text-align: left; font-size: 13px; }}
    .details-table tr:not(:last-child) {{ border-bottom: 1px solid #e2e8f0; }}
    .details-table th {{ padding: 12px 18px; width: 34%; font-weight: 600; color: #64748b; background: #f1f5f9; text-transform: uppercase; font-size: 11px; letter-spacing: 0.5px; }}
    .details-table td {{ padding: 12px 18px; color: #0f172a; font-weight: 500; }}
    .code-badge {{ font-family: monospace; font-weight: bold; color: #4f46e5; background: #eef2ff; padding: 3px 8px; border-radius: 6px; border: 1px solid #c7d2fe; }}
    .cta-container {{ text-align: center; margin: 28px 0; }}
    .cta-button {{ display: inline-block; background: #020617; color: #ffffff !important; text-decoration: none; padding: 14px 32px; border-radius: 12px; font-weight: bold; font-size: 14px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); }}
  </style>
</head>
<body>
  <div class="container">
    {brand_header}
    <div class="content">
      <p style="font-size: 16px; font-weight: 600; color: #0f172a; margin-top: 0;">Dear <strong>{candidate_name}</strong>,</p>
      <p>Your technical interview has been successfully scheduled. Please find your confirmed session details below:</p>

      <div class="table-container">
        <table class="details-table">
          <tr>
            <th>Company / Org</th>
            <td><strong>{company or 'Zavran AI Partner'}</strong></td>
          </tr>
          <tr>
            <th>Target Role</th>
            <td>{role}</td>
          </tr>
          <tr>
            <th>AI Evaluator</th>
            <td>{interviewer_name} <span style="font-size: 11px; color: #64748b;">(AI Technical Evaluator)</span></td>
          </tr>
          <tr>
            <th>Date</th>
            <td>{interview_date}</td>
          </tr>
          <tr>
            <th>Time Slot</th>
            <td>{interview_time} <span style="font-size: 11px; color: #64748b;">(30 min duration)</span></td>
          </tr>
          <tr>
            <th>Room Code</th>
            <td><span class="code-badge">{room_code}</span></td>
          </tr>
        </table>
      </div>

      <p style="font-size: 13px; color: #475569;">
        <strong>Important:</strong> When your interview room is calibrated (~5 minutes prior to the start time), you will receive a follow-up email with the direct access link.
      </p>

      <div class="cta-container">
        <a href="{history_url}" class="cta-button">View Scheduled Session in Portal &rarr;</a>
      </div>

      <p style="font-size: 12px; color: #64748b; text-align: center;">
        Direct link: <a href="{history_url}" style="color: #4f46e5;">{history_url}</a>
      </p>
    </div>
    {footer}
  </div>
</body>
</html>
"""
        return {"subject": subject, "text": text_body, "html": html_body, "url": history_url}

    @classmethod
    async def send_interview_scheduled_email(
        cls,
        to_email: str,
        candidate_name: str,
        room_code: str,
        role: str,
        company: str,
        interviewer_name: str,
        interview_date: str,
        interview_time: str,
        base_url: Optional[str] = None,
    ) -> Dict[str, Any]:
        if not to_email or "@" not in to_email:
            raise ValueError(f"Invalid recipient email address: '{to_email}'")

        content = cls.generate_scheduled_email_content(
            candidate_name=candidate_name,
            room_code=room_code,
            role=role,
            company=company,
            interviewer_name=interviewer_name,
            interview_date=interview_date,
            interview_time=interview_time,
            base_url=base_url,
        )
        provider = cls.get_provider()
        res = await provider.send_email(
            to_email=to_email,
            subject=content["subject"],
            html_body=content["html"],
            text_body=content["text"],
        )
        dispatch_log = {
            "type": "INTERVIEW_SCHEDULED",
            "to_email": to_email,
            "candidate_name": candidate_name,
            "room_code": room_code,
            "timestamp": time.time(),
            "status": "SENT",
            "provider_response": res,
        }
        cls.dispatched_history.append(dispatch_log)
        logger.info(f"Scheduled interview email successfully sent from {get_default_from_email()} to {to_email} for room {room_code}")
        return res

    # -------------------------------------------------------------------------
    # 3. INTERVIEW ROOM READY EMAIL
    # -------------------------------------------------------------------------
    @classmethod
    def generate_interview_ready_email_content(
        cls,
        candidate_name: str,
        room_code: str,
        company: str,
        role: str,
        organization: str,
        interviewer_name: str,
        interview_date: str,
        interview_time: str,
        base_url: Optional[str] = None,
    ) -> Dict[str, str]:
        app_url = base_url or settings.APP_BASE_URL or "http://localhost:8000"
        import urllib.parse
        params = urllib.parse.urlencode({
            "room": room_code,
            "role": role,
            "interviewer": interviewer_name,
            "org": organization or company,
        })
        room_url = f"{app_url}/interview-room.html?{params}"
        subject = f"Your Interview Room is Ready — {role} at {company or organization or 'Zavran AI'}"

        text_body = f"""ZAVRAN AI — INTERVIEW ROOM READY

Hi {candidate_name},

Your AI technical interview room is now calibrated and ready.

============================================================
SESSION DETAILS
============================================================
Company:       {company or organization or 'Zavran AI Partner'}
Role:          {role}
Interviewer:   {interviewer_name} (AI Technical Evaluator)
Date:          {interview_date}
Time:          {interview_time}
Room Code:     {room_code}
============================================================

Access Your Interview Room:
{room_url}

Please join 2–3 minutes before your start time. Ensure your camera and microphone permissions are enabled.

Best regards,
Zavran AI Engineering Team
support.zarvanai@gmail.com
"""

        brand_header = _render_email_brand_header(subtitle="Calibration Ready • Join Room")
        footer = _render_email_footer()

        html_body = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>{subject}</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #0f172a; margin: 0; padding: 24px; color: #1e293b; }}
    .container {{ max-width: 600px; margin: 0 auto; background: #ffffff; border-radius: 20px; overflow: hidden; box-shadow: 0 10px 25px rgba(0,0,0,0.12); border: 1px solid #e2e8f0; }}
    .content {{ padding: 28px; font-size: 14px; line-height: 1.6; color: #334155; }}
    .table-container {{ margin: 20px 0; border: 1px solid #e2e8f0; border-radius: 14px; overflow: hidden; background: #f8fafc; }}
    .details-table {{ width: 100%; border-collapse: collapse; text-align: left; font-size: 13px; }}
    .details-table tr:not(:last-child) {{ border-bottom: 1px solid #e2e8f0; }}
    .details-table th {{ padding: 12px 18px; width: 34%; font-weight: 600; color: #64748b; background: #f1f5f9; text-transform: uppercase; font-size: 11px; letter-spacing: 0.5px; }}
    .details-table td {{ padding: 12px 18px; color: #0f172a; font-weight: 500; }}
    .code-badge {{ font-family: monospace; font-weight: bold; color: #4f46e5; background: #eef2ff; padding: 3px 8px; border-radius: 6px; border: 1px solid #c7d2fe; }}
    .cta-container {{ text-align: center; margin: 28px 0; }}
    .cta-button {{ display: inline-block; background: #020617; color: #ffffff !important; text-decoration: none; padding: 14px 32px; border-radius: 12px; font-weight: bold; font-size: 14px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); }}
  </style>
</head>
<body>
  <div class="container">
    {brand_header}
    <div class="content">
      <p style="font-size: 16px; font-weight: 600; color: #0f172a; margin-top: 0;">Hi <strong>{candidate_name}</strong>,</p>
      <p>Your upcoming AI technical interview room is calibrated and ready. Please find the confirmed session details below:</p>

      <div class="table-container">
        <table class="details-table">
          <tr>
            <th>Company / Org</th>
            <td><strong>{company or organization or 'Zavran AI Partner'}</strong></td>
          </tr>
          <tr>
            <th>Role</th>
            <td>{role}</td>
          </tr>
          <tr>
            <th>AI Evaluator</th>
            <td>{interviewer_name} <span style="font-size: 11px; color: #64748b;">(AI Technical Evaluator)</span></td>
          </tr>
          <tr>
            <th>Date</th>
            <td>{interview_date}</td>
          </tr>
          <tr>
            <th>Time</th>
            <td>{interview_time}</td>
          </tr>
          <tr>
            <th>Room Code</th>
            <td><span class="code-badge">{room_code}</span></td>
          </tr>
        </table>
      </div>

      <div class="cta-container">
        <a href="{room_url}" class="cta-button">Enter Interview Room &rarr;</a>
      </div>

      <p style="font-size: 12px; color: #64748b; text-align: center;">
        Direct Room URL: <a href="{room_url}" style="color: #4f46e5;">{room_url}</a>
      </p>
    </div>
    {footer}
  </div>
</body>
</html>
"""
        return {"subject": subject, "text": text_body, "html": html_body, "url": room_url}

    @classmethod
    async def send_interview_ready_email(
        cls,
        to_email: str,
        candidate_name: str,
        room_code: str,
        company: str,
        role: str,
        organization: str,
        interviewer_name: str,
        interview_date: str,
        interview_time: str,
        base_url: Optional[str] = None,
    ) -> Dict[str, Any]:
        if not to_email or "@" not in to_email:
            raise ValueError(f"Invalid recipient email address: '{to_email}'")

        content = cls.generate_interview_ready_email_content(
            candidate_name=candidate_name,
            room_code=room_code,
            company=company,
            role=role,
            organization=organization,
            interviewer_name=interviewer_name,
            interview_date=interview_date,
            interview_time=interview_time,
            base_url=base_url,
        )
        provider = cls.get_provider()
        res = await provider.send_email(
            to_email=to_email,
            subject=content["subject"],
            html_body=content["html"],
            text_body=content["text"],
        )
        dispatch_log = {
            "type": "INTERVIEW_READY",
            "to_email": to_email,
            "candidate_name": candidate_name,
            "room_code": room_code,
            "timestamp": time.time(),
            "status": "SENT",
            "provider_response": res,
        }
        cls.dispatched_history.append(dispatch_log)
        logger.info(f"Interview-ready email successfully sent from {get_default_from_email()} to {to_email} for room {room_code}")
        return res

    # -------------------------------------------------------------------------
    # 4. INTERVIEW COMPLETED EMAIL (Immediate post-interview confirmation)
    # -------------------------------------------------------------------------
    @classmethod
    def generate_interview_completed_email_content(
        cls,
        candidate_name: str,
        room_code: str,
        role: str,
        organization: str,
        duration_str: str = "30 minutes",
        base_url: Optional[str] = None,
    ) -> Dict[str, str]:
        app_url = base_url or settings.APP_BASE_URL or "http://localhost:8000"
        history_url = f"{app_url}/candidate-portal.html#history"
        subject = f"Interview Completed — {role} Session Submitted (Zavran AI)"

        text_body = f"""ZAVRAN AI — INTERVIEW SESSION COMPLETED

Dear {candidate_name},

Thank you for completing your technical interview session for {role} at {organization or 'Zavran AI'}.

Your responses, audio transcripts, and proctoring audit metrics have been securely submitted to our backend evaluation pipeline.

============================================================
SESSION SUMMARY
============================================================
Role:             {role}
Organization:     {organization or 'Zavran AI Partner'}
Room Code:        {room_code}
Duration:         {duration_str}
Evaluation Status: Processing in Background (~10 minutes)
============================================================

What Happens Next?
Our multi-agent evaluation engine is currently analyzing your technical answers across:
- Architectural and systems design accuracy
- Trade-off articulation and consistency
- Depth taxonomy rating (Level 1 Surface to Level 5 Expert)
- Specific strengths and concrete recommendations for improvement

Your comprehensive Review & Feedback Report will be prepared and delivered to your registered email in approximately 10 minutes.

Track your evaluation progress in the Candidate Portal:
{history_url}

Best regards,
Zavran AI Evaluation Team
support.zarvanai@gmail.com
"""

        brand_header = _render_email_brand_header(subtitle="Interview Completed • Evaluation In Progress")
        footer = _render_email_footer()

        html_body = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>{subject}</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #0f172a; margin: 0; padding: 24px; color: #1e293b; }}
    .container {{ max-width: 600px; margin: 0 auto; background: #ffffff; border-radius: 20px; overflow: hidden; box-shadow: 0 10px 25px rgba(0,0,0,0.12); border: 1px solid #e2e8f0; }}
    .content {{ padding: 28px; font-size: 14px; line-height: 1.6; color: #334155; }}
    .status-banner {{ background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 14px; padding: 16px 20px; margin: 20px 0; display: flex; align-items: center; justify-content: space-between; }}
    .status-title {{ font-size: 13px; font-weight: bold; color: #1e40af; }}
    .status-subtitle {{ font-size: 12px; color: #3b82f6; }}
    .table-container {{ margin: 20px 0; border: 1px solid #e2e8f0; border-radius: 14px; overflow: hidden; background: #f8fafc; }}
    .details-table {{ width: 100%; border-collapse: collapse; text-align: left; font-size: 13px; }}
    .details-table tr:not(:last-child) {{ border-bottom: 1px solid #e2e8f0; }}
    .details-table th {{ padding: 12px 18px; width: 34%; font-weight: 600; color: #64748b; background: #f1f5f9; text-transform: uppercase; font-size: 11px; letter-spacing: 0.5px; }}
    .details-table td {{ padding: 12px 18px; color: #0f172a; font-weight: 500; }}
    .code-badge {{ font-family: monospace; font-weight: bold; color: #4f46e5; background: #eef2ff; padding: 3px 8px; border-radius: 6px; border: 1px solid #c7d2fe; }}
    .cta-container {{ text-align: center; margin: 28px 0; }}
    .cta-button {{ display: inline-block; background: #020617; color: #ffffff !important; text-decoration: none; padding: 14px 32px; border-radius: 12px; font-weight: bold; font-size: 14px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); }}
  </style>
</head>
<body>
  <div class="container">
    {brand_header}
    <div class="content">
      <p style="font-size: 16px; font-weight: 600; color: #0f172a; margin-top: 0;">Dear <strong>{candidate_name}</strong>,</p>
      <p>Thank you for completing your technical interview session. Your responses have been submitted successfully.</p>

      <div class="status-banner">
        <div>
          <div class="status-title">⏳ Multi-Agent Evaluation In Progress</div>
          <div class="status-subtitle">Detailed review report generating in ~10 minutes</div>
        </div>
      </div>

      <div class="table-container">
        <table class="details-table">
          <tr>
            <th>Role</th>
            <td>{role}</td>
          </tr>
          <tr>
            <th>Organization</th>
            <td>{organization or 'Zavran AI Partner'}</td>
          </tr>
          <tr>
            <th>Room Code</th>
            <td><span class="code-badge">{room_code}</span></td>
          </tr>
          <tr>
            <th>Duration</th>
            <td>{duration_str}</td>
          </tr>
        </table>
      </div>

      <p style="font-size: 13px; color: #475569;">
        Our AI scoring engine is evaluating your architectural decisions, trade-offs, and concept depth. Once ready, your full <strong>Interview Feedback Report</strong> will be sent automatically to this email.
      </p>

      <div class="cta-container">
        <a href="{history_url}" class="cta-button">View Portal Dashboard &rarr;</a>
      </div>

      <p style="font-size: 12px; color: #64748b; text-align: center;">
        Direct Portal link: <a href="{history_url}" style="color: #4f46e5;">{history_url}</a>
      </p>
    </div>
    {footer}
  </div>
</body>
</html>
"""
        return {"subject": subject, "text": text_body, "html": html_body, "url": history_url}

    @classmethod
    async def send_interview_completed_email(
        cls,
        to_email: str,
        candidate_name: str,
        room_code: str,
        role: str,
        organization: str,
        duration_str: str = "30 minutes",
        base_url: Optional[str] = None,
    ) -> Dict[str, Any]:
        if not to_email or "@" not in to_email:
            raise ValueError(f"Invalid recipient email address: '{to_email}'")

        content = cls.generate_interview_completed_email_content(
            candidate_name=candidate_name,
            room_code=room_code,
            role=role,
            organization=organization,
            duration_str=duration_str,
            base_url=base_url,
        )
        provider = cls.get_provider()
        res = await provider.send_email(
            to_email=to_email,
            subject=content["subject"],
            html_body=content["html"],
            text_body=content["text"],
        )
        dispatch_log = {
            "type": "INTERVIEW_COMPLETED",
            "to_email": to_email,
            "candidate_name": candidate_name,
            "room_code": room_code,
            "timestamp": time.time(),
            "status": "SENT",
            "provider_response": res,
        }
        cls.dispatched_history.append(dispatch_log)
        logger.info(f"Interview completed confirmation email successfully sent from {get_default_from_email()} to {to_email} for room {room_code}")
        return res

    # -------------------------------------------------------------------------
    # 5. INTERVIEW REVIEW & FEEDBACK REPORT EMAIL (10-Minute Delivery)
    # -------------------------------------------------------------------------
    @classmethod
    def generate_report_email_content(
        cls,
        candidate_name: str,
        report_id: str,
        report: Dict[str, Any],
        base_url: Optional[str] = None,
    ) -> Dict[str, str]:
        app_url = base_url or settings.APP_BASE_URL or "http://localhost:8000"
        secure_report_url = f"{app_url}/interview-report/{report_id}"

        overall_score = report.get("overall_score", 88)
        status = report.get("status") or report.get("recommendation") or "Qualified — Recommended for Hire"
        target_role = report.get("role") or report.get("target_role") or "Full Stack AI Engineer"
        interviewer_name = report.get("interviewer") or "Zaroon AI"
        summary_text = report.get("summary") or "Candidate demonstrated sound understanding of core engineering principles."

        subject = f"Your Zavran AI Interview Feedback Report — {target_role} ({overall_score}/100)"

        text_body = f"""Hi {candidate_name},

Thank you for completing your interview with Zavran AI for the {target_role} position.

Your comprehensive interview feedback report has been generated and is now ready.

============================================================
EVALUATION OVERVIEW
============================================================
Target Role:          {target_role}
Evaluated by:         {interviewer_name}
Overall Rigor Score:  {overall_score}/100
Assessment Status:    {status}
Session ID:           {report_id}
============================================================

Executive Summary:
{summary_text}

The report includes:
- Key strengths verified with concrete interview evidence
- Areas for improvement and missing concept guidance
- Technical topic analysis across system architecture & safety
- Concept-level evaluation and correctness
- Depth of understanding (Level 1 Surface to Level 5 Expert)
- Actionable recommended study & practice focus areas

View Your Complete Interactive Report:
{secure_report_url}

Regards,
Zavran AI Engineering Team
support.zarvanai@gmail.com
"""

        brand_header = _render_email_brand_header(subtitle="Interview Feedback Report • 10-Min Review")
        footer = _render_email_footer()

        html_body = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>{subject}</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #0f172a; margin: 0; padding: 24px; color: #1e293b; }}
    .container {{ max-width: 600px; margin: 0 auto; background: #ffffff; border-radius: 20px; overflow: hidden; box-shadow: 0 10px 25px rgba(0,0,0,0.12); border: 1px solid #e2e8f0; }}
    .content {{ padding: 28px; font-size: 14px; line-height: 1.6; color: #334155; }}
    .score-card {{ background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 16px; padding: 20px; margin: 20px 0; display: flex; align-items: center; justify-content: space-between; }}
    .score-val {{ font-size: 32px; font-weight: 900; color: #10b981; font-family: monospace; }}
    .score-label {{ font-size: 11px; font-weight: bold; text-transform: uppercase; color: #64748b; font-family: monospace; }}
    .status-pill {{ display: inline-block; padding: 3px 10px; background: #ecfdf5; border: 1px solid #a7f3d0; border-radius: 999px; font-size: 11px; font-weight: bold; color: #065f46; }}
    .checklist {{ margin: 16px 0; padding-left: 20px; color: #475569; }}
    .checklist li {{ margin-bottom: 6px; }}
    .cta-container {{ text-align: center; margin: 28px 0; }}
    .cta-button {{ display: inline-block; background: #020617; color: #ffffff !important; text-decoration: none; padding: 14px 28px; border-radius: 12px; font-weight: bold; font-size: 14px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); }}
  </style>
</head>
<body>
  <div class="container">
    {brand_header}
    <div class="content">
      <p style="font-size: 16px; font-weight: 600; color: #0f172a; margin-top: 0;">Hi <strong>{candidate_name}</strong>,</p>

      <p>Thank you for completing your interview with Zavran AI for the <strong>{target_role}</strong> position.</p>
      <p>Your detailed 10-minute interview feedback report is now compiled and ready for review.</p>

      <div class="score-card">
        <div>
          <div class="score-label">Overall Rigor Score</div>
          <div class="score-val">{overall_score}<span style="font-size: 16px; color: #94a3b8; font-weight: normal;">/100</span></div>
        </div>
        <div style="text-align: right;">
          <div class="status-pill">{status}</div>
        </div>
      </div>

      <p><strong>The report includes:</strong></p>
      <ul class="checklist">
        <li><strong>Key strengths:</strong> Concrete architectural capabilities verified with evidence.</li>
        <li><strong>Areas for improvement:</strong> Specific technical gaps, missing concepts, and concrete guidance.</li>
        <li><strong>Technical topic analysis:</strong> Domain mastery across system design, safety guardrails, and economics.</li>
        <li><strong>Depth of understanding:</strong> Level 1 Surface to Level 5 Expert taxonomy classification.</li>
        <li><strong>Cross-question consistency:</strong> Articulation of trade-offs across questions.</li>
        <li><strong>Recommended focus areas:</strong> Actionable study and practice recommendations.</li>
      </ul>

      <div class="cta-container">
        <a href="{secure_report_url}" class="cta-button">View Your Full Interview Report &rarr;</a>
      </div>

      <p style="font-size: 12px; color: #64748b; text-align: center;">
        Direct link: <a href="{secure_report_url}" style="color: #4f46e5;">{secure_report_url}</a>
      </p>
    </div>
    {footer}
  </div>
</body>
</html>
"""
        return {
            "subject": subject,
            "text": text_body,
            "html": html_body,
            "url": secure_report_url,
        }

    @classmethod
    async def send_candidate_report_email(
        cls,
        to_email: str,
        candidate_name: str,
        report_id: str,
        report: Dict[str, Any],
        base_url: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Sends the final candidate report email."""
        if not to_email or "@" not in to_email:
            raise ValueError(f"Invalid recipient email address: '{to_email}'")

        content = cls.generate_report_email_content(
            candidate_name=candidate_name,
            report_id=report_id,
            report=report,
            base_url=base_url,
        )

        provider = cls.get_provider()
        res = await provider.send_email(
            to_email=to_email,
            subject=content["subject"],
            html_body=content["html"],
            text_body=content["text"],
        )

        dispatch_log = {
            "type": "INTERVIEW_REPORT",
            "to_email": to_email,
            "candidate_name": candidate_name,
            "report_id": report_id,
            "timestamp": time.time(),
            "status": "SENT",
            "provider_response": res,
        }
        cls.dispatched_history.append(dispatch_log)
        logger.info(f"Report email successfully sent from {get_default_from_email()} to verified Clerk email: {to_email} for session {report_id}")
        return res

