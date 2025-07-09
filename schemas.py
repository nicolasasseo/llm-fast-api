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
