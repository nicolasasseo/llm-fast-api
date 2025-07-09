"""Database configuration and session helpers.

Initialises the SQLAlchemy engine from the DATABASE_URL environment variable
and exposes a `get_db` generator dependency for FastAPI routes.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:postgres@localhost:5432/chatapi",  # Default placeholder
)

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Create a configured "Session" class
SessionLocal = sessionmaker(bind=engine)

# Base class for declarative models
Base = declarative_base()


def get_db():
    """FastAPI dependency that provides a SQLAlchemy session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
