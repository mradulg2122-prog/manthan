"""
Application configuration.
Loads settings from environment variables / .env file.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """All app settings — loaded from .env automatically."""

    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/eventflow_pro"

    # App
    APP_NAME: str = "EventFlow Pro"
    DEBUG: bool = True
    SECRET_KEY: str = "change-me-in-production"

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    class Config:
        env_file = ".env"


# Single instance used across the app
settings = Settings()
