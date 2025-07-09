"""CRUD (Create-Read-Update-Delete) helpers for Conversation records.

These functions wrap SQLAlchemy operations so that database access is kept
separate from the FastAPI route handlers.
"""

from sqlalchemy.orm import Session

import models


def create_conversation(db: Session, prompt: str, response: str) -> models.Conversation:
    """Create a new conversation record in the database."""
    db_convo = models.Conversation(prompt=prompt, response=response)
    db.add(db_convo)
    db.commit()
    db.refresh(db_convo)
    return db_convo


def get_conversation(db: Session, conversation_id: int) -> models.Conversation | None:
    return (
        db.query(models.Conversation)
        .filter(models.Conversation.id == conversation_id)
        .first()
    )


def list_conversations(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Conversation)
        .order_by(models.Conversation.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
