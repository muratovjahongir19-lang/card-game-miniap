"""
Database connection and session management
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from bot.config import settings

# Create engine
engine = create_engine(
    settings.database_url,
    echo=settings.debug,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Base class for models
Base = declarative_base()


def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)


def get_session():
    """Get database session"""
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()
