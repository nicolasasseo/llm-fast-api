"""CRUD (Create-Read-Update-Delete) helpers for User, ChatSession, and Message records.

These functions wrap SQLAlchemy operations so that database access is kept
separate from the FastAPI route handlers.
"""

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import models
import schemas
from typing import List, Optional
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username, email=user.email, hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_id(db: Session, user_id: int) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.username == username).first()


def create_chat_session(
    db: Session, chat_session: schemas.ChatSessionCreate
) -> models.ChatSession:
    db_session = models.ChatSession(user_id=chat_session.user_id)
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session


def get_chat_sessions_by_user(db: Session, user_id: int) -> List[models.ChatSession]:
    return (
        db.query(models.ChatSession)
        .filter(models.ChatSession.user_id == user_id)
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
