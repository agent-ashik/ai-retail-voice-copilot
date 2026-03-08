"""
Database connection and session management.
"""

from contextlib import contextmanager
from typing import Generator
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import Pool

from .config import settings
from .logging_config import get_logger
from .exceptions import DatabaseException

logger = get_logger(__name__)


# Create database engine
engine = create_engine(
    settings.database_url,
    pool_size=settings.database_pool_size,
    max_overflow=settings.database_max_overflow,
    pool_pre_ping=True,  # Verify connections before using
    echo=settings.debug,  # Log SQL queries in debug mode
)


# Listen for connection events
@event.listens_for(Pool, "connect")
def set_sqlite_pragma(dbapi_conn, connection_record):
    """Set SQLite pragmas for better performance (if using SQLite)."""
    if "sqlite" in settings.database_url:
        cursor = dbapi_conn.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db() -> Generator[Session, None, None]:
    """
    Dependency function to get database session.
    
    Yields:
        Session: SQLAlchemy database session
        
    Example:
        @app.get("/items")
        def get_items(db: Session = Depends(get_db)):
            return db.query(Item).all()
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error("database_session_error", error=str(e))
        db.rollback()
        raise DatabaseException(f"Database session error: {str(e)}")
    finally:
        db.close()


@contextmanager
def get_db_context() -> Generator[Session, None, None]:
    """
    Context manager for database sessions.
    
    Yields:
        Session: SQLAlchemy database session
        
    Example:
        with get_db_context() as db:
            items = db.query(Item).all()
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        logger.error("database_context_error", error=str(e))
        db.rollback()
        raise DatabaseException(f"Database transaction error: {str(e)}")
    finally:
        db.close()


def init_db() -> None:
    """Initialize database tables."""
    from .models import Base
    
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("database_initialized", message="Database tables created successfully")
    except Exception as e:
        logger.error("database_init_error", error=str(e))
        raise DatabaseException(f"Failed to initialize database: {str(e)}")


def drop_db() -> None:
    """Drop all database tables. Use with caution!"""
    from .models import Base
    
    try:
        Base.metadata.drop_all(bind=engine)
        logger.warning("database_dropped", message="All database tables dropped")
    except Exception as e:
        logger.error("database_drop_error", error=str(e))
        raise DatabaseException(f"Failed to drop database: {str(e)}")
