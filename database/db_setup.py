from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Database file path
DB_PATH = os.path.join(os.path.dirname(__file__), "smartpos.db")
DB_URL = f"sqlite:///{DB_PATH}"

# Create engine
engine = create_engine(DB_URL, echo=False, connect_args={"check_same_thread": False})

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

def init_db():
    """Initialize the database and create all tables."""
    from database import models
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully.")
