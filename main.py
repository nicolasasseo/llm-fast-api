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


@app.post("/generate", response_model=schemas.GenerateResponse)
def generate_text(
    request: schemas.GenerateRequest,
    db: Session = Depends(database.get_db),
):
    """Generate a completion from the language model and store it in DB."""
    try:
        response_text = llm.generate(
            prompt=request.prompt,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    conversation = crud.create_conversation(
        db, prompt=request.prompt, response=response_text
    )

    return schemas.GenerateResponse.model_validate(conversation)


@app.get("/conversations/{conversation_id}", response_model=schemas.GenerateResponse)
def read_conversation(conversation_id: int, db: Session = Depends(database.get_db)):
    conversation = crud.get_conversation(db, conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return schemas.GenerateResponse.model_validate(conversation)


@app.get("/conversations", response_model=list[schemas.GenerateResponse])
def list_conversations(
    skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)
):
    conversations = crud.list_conversations(db, skip=skip, limit=limit)
    return [schemas.GenerateResponse.model_validate(c) for c in conversations]
