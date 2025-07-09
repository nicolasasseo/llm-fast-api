"""Pydantic request/response schemas used by the API endpoints."""

from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class GenerateRequest(BaseModel):
    prompt: str = Field(..., description="User prompt to send to LLM")
    max_tokens: int = Field(128, description="Maximum number of tokens to generate")
    temperature: float = Field(0.7, description="Sampling temperature")


class GenerateResponse(BaseModel):
    id: int
    prompt: str
    response: str
    created_at: datetime

    # Enable attribute-based validation for ORM objects
    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    username: str = Field(..., description="Unique username")
    email: str = Field(..., description="User email")
    password: str = Field(..., description="User password")


class UserRead(BaseModel):
    id: int
    username: str
    email: str
    model_config = ConfigDict(from_attributes=True)


class ChatSessionCreate(BaseModel):
    # Optionally allow naming sessions, or just use user_id
    user_id: int = Field(..., description="ID of the user starting the session")


class ChatSessionRead(BaseModel):
    id: int
    user_id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class MessageCreate(BaseModel):
    chat_session_id: int = Field(..., description="ID of the chat session")
    sender: str = Field(..., description='"user" or "assistant"')
    content: str = Field(..., description="Message content")


class MessageRead(BaseModel):
    id: int
    chat_session_id: int
    sender: str
    content: str
    timestamp: datetime
    model_config = ConfigDict(from_attributes=True)
