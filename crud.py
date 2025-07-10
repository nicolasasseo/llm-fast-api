"""CRUD (Create-Read-Update-Delete) helpers for User, ChatSession, and Message records.

These functions wrap SQLAlchemy operations so that database access is kept
separate from the FastAPI route handlers.
"""

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import models
import schemas
from typing import List, Optional


def create_chat_session(
    db: Session, chat_session: schemas.ChatSessionCreate
) -> models.ChatSession:
    db_session = models.ChatSession()
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session


def get_chat_sessions(db: Session) -> List[models.ChatSession]:
    return (
        db.query(models.ChatSession)
        .order_by(models.ChatSession.created_at.desc())
        .all()
    )


def create_message(db: Session, message: schemas.MessageCreate) -> models.Message:
    db_message = models.Message(
        chat_session_id=message.chat_session_id,
        sender=message.sender,
        content=message.content,
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


def get_messages_by_session(db: Session, chat_session_id: int) -> List[models.Message]:
    return (
        db.query(models.Message)
        .filter(models.Message.chat_session_id == chat_session_id)
        .order_by(models.Message.timestamp.asc())
        .all()
    )
