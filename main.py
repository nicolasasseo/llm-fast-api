"""Simple FastAPI application for chat with LLM using in-memory conversation history."""

from fastapi import FastAPI
import schemas
import llm
import logging
import os
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise RuntimeError("API_KEY not set in environment variables")


# Dependency for API key authentication
class APIKeyAuth(HTTPBearer):
    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:
        credentials = await super().__call__(request)
        if (
            credentials is None
            or credentials.scheme.lower() != "bearer"
            or credentials.credentials != API_KEY
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or missing API Key",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return credentials


api_key_auth = APIKeyAuth()

logging.basicConfig(level=logging.INFO)
logging.info("Context length: %s", llm.get_context_length())
from fastapi.responses import StreamingResponse

app = FastAPI(title="Simple Chat API", version="0.1.0")


# In-memory conversation history
conversation_history = []


@app.post("/chat", response_model=schemas.ChatResponse)
def chat(
    request: schemas.ChatRequest,
    credentials: HTTPAuthorizationCredentials = Depends(api_key_auth),
):
    """Send a message and get LLM response with conversation history."""
    global conversation_history

    # Initialize conversation with system prompt if empty
    if not conversation_history:
        conversation_history.append(
            {"role": "system", "content": request.system_prompt}
        )

    # Update system prompt if it has changed

    if (
        conversation_history
        and request.system_prompt != conversation_history[0]["content"]
    ):
        logging.info("System prompt has changed")
        conversation_history.pop(0)
        conversation_history.insert(
            0, {"role": "system", "content": request.system_prompt}
        )
    else:
        logging.info("System prompt has not changed")

    # Add user message to history
    conversation_history.append({"role": "user", "content": request.message})

    # Get LLM response
    assistant_response = llm.generate(messages=conversation_history)

    # Add assistant response to history
    conversation_history.append({"role": "assistant", "content": assistant_response})

    return schemas.ChatResponse(
        response=assistant_response, history=conversation_history
    )


@app.post("/chat/stream")
def chat_stream(
    request: schemas.ChatRequest,
    credentials: HTTPAuthorizationCredentials = Depends(api_key_auth),
):
    global conversation_history

    # Initialize conversation with system prompt if empty
    if not conversation_history:
        conversation_history.append(
            {"role": "system", "content": request.system_prompt}
        )

    # Update system prompt if it has changed
    if (
        conversation_history
        and request.system_prompt != conversation_history[0]["content"]
    ):
        conversation_history[0]["content"] = request.system_prompt

    # Add user message to history
    conversation_history.append({"role": "user", "content": request.message})

    # Define a generator that yields the response as it streams
    def response_generator():
        response_chunks = []
        for chunk in llm.generate_stream(messages=conversation_history):
            response_chunks.append(chunk)
            yield chunk
        full_response = "".join(response_chunks)
        conversation_history.append({"role": "assistant", "content": full_response})

    return StreamingResponse(response_generator(), media_type="text/plain")
