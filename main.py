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

logging.basicConfig(
    level=logging.INFO,
    filename="fastapi.log",  # Log to this file
    filemode="a",  # Append to the file
    format="%(asctime)s %(levelname)s %(message)s",
)
logging.info("Context length: %s", llm.get_context_length())
from fastapi.responses import StreamingResponse

app = FastAPI(title="Simple Chat API", version="0.1.0")


# In-memory conversation history


@app.post("/chat", response_model=schemas.ChatResponse)
def chat(
    request: schemas.ChatRequest,
    credentials: HTTPAuthorizationCredentials = Depends(api_key_auth),
):
    """Send a message and get LLM response with conversation history."""
    message = {"role": "user", "content": request.message}
    request.history.append(message)

    system_message = {"role": "system", "content": request.system_prompt}
    messages = [system_message] + request.history

    # Optionally filter out empty content messages as discussed before
    messages = [msg for msg in messages if msg.get("content")]

    print(f"Messages: {messages}")

    # Get LLM response
    assistant_response = llm.generate(messages=messages)

    # Add assistant response to history
    request.history.append({"role": "assistant", "content": assistant_response})

    return schemas.ChatResponse(response=assistant_response, history=request.history)


@app.post("/chat/stream")
def chat_stream(
    request: schemas.ChatRequest,
    credentials: HTTPAuthorizationCredentials = Depends(api_key_auth),
):
    message = {"role": "user", "content": request.message}
    request.history.append(message)

    system_message = {"role": "system", "content": request.system_prompt}
    messages = [system_message] + request.history

    # Optionally filter out empty content messages as discussed before
    messages = [msg for msg in messages if msg.get("content")]

    # Define a generator that yields the response as it streams
    def response_generator():
        response_chunks = []
        for chunk in llm.generate_stream(messages=messages):
            response_chunks.append(chunk)
            yield chunk
        full_response = "".join(response_chunks)
        request.history.append({"role": "assistant", "content": full_response})

    return StreamingResponse(response_generator(), media_type="text/plain")
