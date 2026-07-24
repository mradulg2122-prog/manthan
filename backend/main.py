"""
EventFlow Pro — Main application entry point.

Run with:
    uvicorn backend.main:app --reload
"""

import logging
from datetime import datetime, timezone

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config import settings

# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
)
logger = logging.getLogger("eventflow")

# ---------------------------------------------------------------------------
# App instance  (Swagger UI is enabled by default at /docs)
# ---------------------------------------------------------------------------
app = FastAPI(
    title=settings.APP_NAME,
    version="0.1.0",
    description="AI-powered event management platform.",
    docs_url="/docs",        # Swagger UI
    redoc_url="/redoc",      # ReDoc
)

# ---------------------------------------------------------------------------
# CORS — allow all origins during development
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     # lock this down in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Startup / shutdown events
# ---------------------------------------------------------------------------
@app.on_event("startup")
async def on_startup():
    logger.info("🚀 %s is starting …", settings.APP_NAME)


@app.on_event("shutdown")
async def on_shutdown():
    logger.info("👋 %s is shutting down …", settings.APP_NAME)


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.get("/", tags=["Root"])
async def root():
    """Welcome endpoint — confirms the API is reachable."""
    return {
        "app": settings.APP_NAME,
        "version": "0.1.0",
        "message": "Welcome to EventFlow Pro API",
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health-check endpoint for monitoring / load-balancers."""
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "debug": settings.DEBUG,
    }
