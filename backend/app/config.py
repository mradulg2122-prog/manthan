"""
Application configuration.
Loads settings from .env file using python-dotenv.
"""

import os
from dotenv import load_dotenv

# Load .env file from the backend/ directory
load_dotenv()


class Settings:
    """All app settings — read from environment variables."""

    APP_NAME: str = os.getenv("APP_NAME", "EventFlow Pro")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    DATABASE_URL: str = os.getenv("DATABASE_URL") or "sqlite:///./eventflow.db"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-me-in-production")

    # SMTP (for sending QR emails — works locally, blocked on Render)
    SMTP_HOST: str = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_EMAIL: str = os.getenv("SMTP_EMAIL", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")

    # Resend (HTTP-based email — works on Render and all platforms)
    RESEND_API_KEY: str = os.getenv("RESEND_API_KEY", "")
    RESEND_FROM_EMAIL: str = os.getenv("RESEND_FROM_EMAIL", "EventFlow <onboarding@resend.dev>")


# Single instance used across the app
settings = Settings()
