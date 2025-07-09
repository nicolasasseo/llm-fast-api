"""SQLAlchemy ORM models defining the application's relational schema."""

from sqlalchemy import Column, Integer, Text, DateTime
from sqlalchemy.sql import func

from database import Base


class Conversation(Base):
    """Stores user prompts and LLM responses"""

    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    prompt = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
