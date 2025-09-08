from sqlmodel import create_engine, Session
from backend.storage.models import SQLModel
from config import get_settings
from typing import Generator
from contextlib import contextmanager

engine = create_engine(f"sqlite:///{get_settings().database_uri}")


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
