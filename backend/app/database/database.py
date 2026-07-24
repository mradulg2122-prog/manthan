"""
Database connection setup.
Creates the SQLAlchemy engine, session factory, and Base class.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config import settings

# ---------------------------------------------------------------------------
# Engine — connects to DB using DATABASE_URL from .env or SQLite fallback
# ---------------------------------------------------------------------------
db_url = settings.DATABASE_URL or "sqlite:///./eventflow.db"
connect_args = {"check_same_thread": False} if db_url.startswith("sqlite") else {}

engine = create_engine(db_url, echo=settings.DEBUG, connect_args=connect_args)

# ---------------------------------------------------------------------------
# Session factory — each request gets its own session via get_db()
# ---------------------------------------------------------------------------
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# ---------------------------------------------------------------------------
# Base class — all models inherit from this
# ---------------------------------------------------------------------------
Base = declarative_base()


# ---------------------------------------------------------------------------
# Dependency — use in FastAPI routes: db: Session = Depends(get_db)
# ---------------------------------------------------------------------------
def get_db():
    """Yield a database session, then close it when the request is done."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------------------------------------------------------------------
# Table creation — call once at startup
# ---------------------------------------------------------------------------
def create_tables():
    """Create all tables that don't exist yet."""
    Base.metadata.create_all(bind=engine)
