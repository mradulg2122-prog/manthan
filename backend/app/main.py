"""
EventFlow Pro — FastAPI entry point.

Run from the backend/ folder:
    uvicorn app.main:app --reload
"""

import logging
import smtplib

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.database.database import create_tables
from app.models.participant import Participant  # noqa: F401 — registers model with Base
from app.models.user import User  # noqa: F401 — registers model with Base
from app.api.registration import router as registration_router
from app.api.scan import router as scan_router
from app.api.auth import router as auth_router
from app.api.dashboard import router as dashboard_router
from app.background.watcher import start_watcher, stop_watcher, watcher_is_running
from app.services.auth_service import hash_password

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
)
logger = logging.getLogger("eventflow")

# ---------------------------------------------------------------------------
# FastAPI app  (Swagger UI at /docs, ReDoc at /redoc)
# ---------------------------------------------------------------------------
app = FastAPI(
    title=settings.APP_NAME,
    version="0.1.0",
    description="AI-powered event management platform.",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ---------------------------------------------------------------------------
# CORS — wide open for local development
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Seed default admin + volunteers
# ---------------------------------------------------------------------------
from app.database.database import SessionLocal

MAX_VOLUNTEERS = 3

def seed_admin():
    """Create the default admin user if it doesn't exist."""
    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.email == "admin@eventflow.com").first()
        if not existing:
            admin = User(
                name="Admin",
                email="admin@eventflow.com",
                password=hash_password("admin123"),
                role="ADMIN",
            )
            db.add(admin)
            db.commit()
            logger.info("🔑 Default admin created: admin@eventflow.com")
        else:
            logger.info("🔑 Default admin already exists.")
    finally:
        db.close()


def seed_volunteers():
    """Create default volunteer accounts (max 3) if they don't exist."""
    volunteers = [
        {"name": "Volunteer 1", "email": "volunteer1@eventflow.com", "password": "vol123"},
        {"name": "Volunteer 2", "email": "volunteer2@eventflow.com", "password": "vol123"},
        {"name": "Volunteer 3", "email": "volunteer3@eventflow.com", "password": "vol123"},
    ]
    db = SessionLocal()
    try:
        existing_count = db.query(User).filter(User.role == "VOLUNTEER").count()
        if existing_count >= MAX_VOLUNTEERS:
            logger.info("📱 %d volunteer(s) already exist (max %d).", existing_count, MAX_VOLUNTEERS)
            return

        for v in volunteers:
            if db.query(User).filter(User.email == v["email"]).first():
                continue
            if db.query(User).filter(User.role == "VOLUNTEER").count() >= MAX_VOLUNTEERS:
                break
            user = User(
                name=v["name"],
                email=v["email"],
                password=hash_password(v["password"]),
                role="VOLUNTEER",
            )
            db.add(user)
            db.commit()
            logger.info("📱 Volunteer created: %s", v["email"])
    finally:
        db.close()


# ---------------------------------------------------------------------------
# Startup & shutdown events
# ---------------------------------------------------------------------------
from app.database.database import engine

@app.on_event("startup")
async def on_startup():
    logger.info("🚀 %s is starting ...", settings.APP_NAME)
    logger.info("📌 DATABASE_URL (API & Engine): %s", engine.url)
    create_tables()
    logger.info("✅ Database tables are ready.")
    seed_admin()
    seed_volunteers()
    start_watcher()


# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------
app.include_router(auth_router)
app.include_router(registration_router)
app.include_router(scan_router)
app.include_router(dashboard_router)


@app.on_event("shutdown")
async def on_shutdown():
    stop_watcher()
    logger.info("👋 %s is shutting down ...", settings.APP_NAME)


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint — confirms the API is live."""
    return {
        "project": "EventFlow Pro",
        "status": "running",
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check — reports backend, database, watcher, and email status."""
    import os
    # Database
    db_ok = False
    db_type = "sqlite"
    total_participants = 0
    db = SessionLocal()
    try:
        from sqlalchemy import text
        db.execute(text("SELECT 1"))
        db_ok = True
        total_participants = db.query(Participant).count()
        db_url_str = str(db.get_bind().url)
        if "postgresql" in db_url_str or "postgres" in db_url_str:
            db_type = "postgresql (persistent)"
        else:
            db_type = "sqlite (local/temporary)"
    except Exception:
        pass
    finally:
        db.close()

    # Watcher
    watcher_ok = watcher_is_running()

    # Email config checks
    brevo_key = (os.getenv("BREVO_API_KEY") or os.getenv("BREVO_KEY") or "").strip()
    resend_key = (os.getenv("RESEND_API_KEY") or os.getenv("RESEND_KEY") or "").strip()
    smtp_email = os.getenv("SMTP_EMAIL") or settings.SMTP_EMAIL or ""
    smtp_pwd = os.getenv("SMTP_PASSWORD") or settings.SMTP_PASSWORD or ""

    return {
        "status": "healthy" if (db_ok and watcher_ok) else "degraded",
        "database": {
            "connected": db_ok,
            "engine": db_type,
            "total_participants": total_participants,
            "max_limit": 100,
        },
        "watcher": "running" if watcher_ok else "stopped",
        "email_engines": {
            "brevo_https_port443": {
                "configured": bool(brevo_key),
                "key_preview": (brevo_key[:8] + "...") if brevo_key else "NOT_FOUND",
            },
            "resend_https_port443": {
                "configured": bool(resend_key),
            },
            "gmail_smtp_fallback": {
                "configured": bool(smtp_email and smtp_pwd.strip()),
                "sender": smtp_email or "NOT_SET",
            },
        },
    }



# ---------------------------------------------------------------------------
# Global exception handler
# ---------------------------------------------------------------------------
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error("Unhandled error on %s: %s", request.url.path, exc)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error." if not settings.DEBUG else str(exc)},
    )
