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

    # Gmail API (OAuth 2.0 — works on Render via HTTPS, no SMTP ports needed)
    GMAIL_CLIENT_ID: str = os.getenv("GMAIL_CLIENT_ID", "")
    GMAIL_CLIENT_SECRET: str = os.getenv("GMAIL_CLIENT_SECRET", "")
    GMAIL_REFRESH_TOKEN: str = os.getenv("GMAIL_REFRESH_TOKEN", "")
    GMAIL_SENDER_EMAIL: str = os.getenv("GMAIL_SENDER_EMAIL", "mradulg2122@gmail.com")


# Single instance used across the app
settings = Settings()
