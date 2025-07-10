"""Pydantic request/response schemas for the simple chat API."""

from datetime import datetime
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(..., description="User message to send to LLM")
    system_prompt: str = Field(
        ..., description="System prompt to define the agent's behavior"
    )


class ChatResponse(BaseModel):
    response: str = Field(..., description="LLM's response to the user message")
    history: list[str] = Field(..., description="Full conversation history")


class HistoryResponse(BaseModel):
    history: list[str] = Field(..., description="Full conversation history")
