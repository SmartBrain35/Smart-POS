from sqlmodel import create_engine, Session, SQLModel
from typing import Generator
from contextlib import contextmanager
from pathlib import Path
from sqlalchemy import inspect, text  # Added text here

# ======================
# Database Configuration
# ======================
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "app.db"
DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DATABASE_URL, echo=False)  # echo=True for SQL debug logs


# ======================
# Initialize Database
# ======================
def init_db() -> None:
    """Initialize the database and create all tables if they don't exist."""
    SQLModel.metadata.create_all(engine)
    migrate_db()  # Call migration after creating tables


# NEW: Migration function to handle schema updates
def migrate_db() -> None:
    inspector = inspect(engine)
    if inspector.has_table("stocks"):
        columns = [col["name"] for col in inspector.get_columns("stocks")]
        if "is_active" not in columns:
            with engine.connect() as conn:
                conn.execute(
                    text("ALTER TABLE stocks ADD COLUMN is_active INTEGER DEFAULT 1")
                )

        # Fix category case for existing records (to match Enum)
        with engine.connect() as conn:
            conn.execute(text("UPDATE stocks SET category = LOWER(category)"))
    # Add similar checks for other tables/columns if needed in the future


# ======================
# Session Manager
# ======================
@contextmanager
def get_session() -> Generator[Session, None, None]:
    """
    Context manager for database sessions.
    Usage:
        with get_session() as session:
            session.add(obj)
            session.commit()
    """
    with Session(engine) as session:
        try:
            yield session
        except Exception:
            session.rollback()
            raise
