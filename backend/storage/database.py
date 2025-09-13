from sqlmodel import create_engine, Session
from backend.storage.models import SQLModel
from typing import Generator
from contextlib import contextmanager
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "app.db"
DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DATABASE_URL)

def init_db() -> None:
    """Initialize the database and create all tables if they don't exist"""
    SQLModel.metadata.create_all(engine)


@contextmanager
def get_session() -> Generator[Session, None, None]:
    """Context manager for database sessions"""
    with Session(engine) as session:
        try:
            yield session
        except Exception:
            session.rollback()
            raise
        else:
            session.commit()
