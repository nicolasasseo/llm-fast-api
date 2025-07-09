"""FastAPI application exposing chat generation and conversation history APIs.

The app wires together database models, CRUD helpers, Pydantic schemas, and an
Ollama LLM client to offer a minimal chat completion service.
"""

from fastapi import FastAPI, Depends, HTTPException
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session

import database
import models
import schemas
import crud
import llm


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Run startup and shutdown tasks using FastAPI's lifespan protocol."""
    # Startup: create DB tables
    database.Base.metadata.create_all(bind=database.engine)
    yield
    # (Optional) add any shutdown logic here


app = FastAPI(title="Ollama Chat API", version="0.1.0", lifespan=lifespan)


# --- User Endpoints ---
@app.post("/users", response_model=schemas.UserRead)
def register_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db, user)


@app.get("/users/{user_id}", response_model=schemas.UserRead)
def get_user(user_id: int, db: Session = Depends(database.get_db)):
    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# --- Chat Session Endpoints ---
@app.post("/sessions", response_model=schemas.ChatSessionRead)
def create_chat_session(
    session: schemas.ChatSessionCreate, db: Session = Depends(database.get_db)
):
    user = crud.get_user_by_id(db, session.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.create_chat_session(db, session)


@app.get("/users/{user_id}/sessions", response_model=list[schemas.ChatSessionRead])
def list_chat_sessions(user_id: int, db: Session = Depends(database.get_db)):
    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    sessions = crud.get_chat_sessions_by_user(db, user_id)
    return sessions


# --- Message Endpoints ---
@app.post("/messages", response_model=schemas.MessageRead)
def create_message(
    message: schemas.MessageCreate, db: Session = Depends(database.get_db)
):
    session = (
        db.query(models.ChatSession)
        .filter(models.ChatSession.id == message.chat_session_id)
        .first()
    )
    if not session:
        raise HTTPException(status_code=404, detail="Chat session not found")

    # 1. Store the user's message
    user_msg = crud.create_message(db, message)

    # 2. Call the LLM to generate a response
    assistant_content = llm.generate(prompt=message.content)

    # 3. Store the assistant's response
    assistant_msg = crud.create_message(
        db,
        schemas.MessageCreate(
            chat_session_id=message.chat_session_id,
            sender="assistant",
            content=assistant_content,
        ),
    )

    # 4. Return the assistant's message (or both messages if you want)
    return assistant_msg


@app.get("/sessions/{session_id}/messages", response_model=list[schemas.MessageRead])
def list_messages(session_id: int, db: Session = Depends(database.get_db)):
    session = (
        db.query(models.ChatSession).filter(models.ChatSession.id == session_id).first()
    )
    if not session:
        raise HTTPException(status_code=404, detail="Chat session not found")
    messages = crud.get_messages_by_session(db, session_id)
    return messages
