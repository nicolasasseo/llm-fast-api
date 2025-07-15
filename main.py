"""Simple FastAPI application for chat with LLM using in-memory conversation history."""

from fastapi import FastAPI
import schemas
import llm
import logging

logging.basicConfig(level=logging.INFO)
logging.info("Context length: %s", llm.get_context_length())
from fastapi.responses import StreamingResponse

app = FastAPI(title="Simple Chat API", version="0.1.0")


# In-memory conversation history
conversation_history = []


@app.post("/chat", response_model=schemas.ChatResponse)
def chat(request: schemas.ChatRequest):
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
        print("System prompt has changed")
        conversation_history[0]["content"] = request.system_prompt
    else:
        print("System prompt has not changed")

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
def chat_stream(request: schemas.ChatRequest):
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
