"""SQLAlchemy ORM models defining the application's relational schema."""

from sqlalchemy import Column, Integer, Text, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import datetime


class ChatSession(Base):
    """Represents a chat session belonging to a user."""

    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    messages = relationship("Message", back_populates="chat_session")


class Message(Base):
    """Represents a message in a chat session."""

    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    chat_session_id = Column(Integer, ForeignKey("chat_sessions.id"))
    sender = Column(String)  # "user" or "assistant" or "agent-prompt"
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    chat_session = relationship("ChatSession", back_populates="messages")
