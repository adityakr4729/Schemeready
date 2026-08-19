import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if sys.path and sys.path[0] == current_dir:
    sys.path.pop(0)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from database.models import Base

DB_PATH = os.path.join(parent_dir, "schemeready.db")
DATABASE_URL = os.environ.get("DATABASE_URL", f"sqlite:///{DB_PATH}")

# Set check_same_thread to False for Streamlit concurrency
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Create all database tables if they do not exist."""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Dependency / context helper to yield database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
