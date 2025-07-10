"""Simple FastAPI application for chat with LLM using in-memory conversation history."""

from fastapi import FastAPI
import schemas
import llm

app = FastAPI(title="Simple Chat API", version="0.1.0")

# In-memory conversation history
conversation_history = []


@app.post("/chat", response_model=schemas.ChatResponse)
def chat(request: schemas.ChatRequest):
    """Send a message and get LLM response with conversation history."""
    global conversation_history

    # Initialize conversation with system prompt if empty
    if not conversation_history:
        conversation_history.append(f"System: {request.system_prompt}")

    # Add user message to history
    conversation_history.append(f"User: {request.message}")

    # Build prompt for LLM (all history + prompt for assistant response)
    prompt = "\n".join(conversation_history) + "\nAssistant:"

    # Get LLM response
    assistant_response = llm.generate(prompt=prompt)

    # Add assistant response to history
    conversation_history.append(f"Assistant: {assistant_response}")

    return schemas.ChatResponse(
        response=assistant_response, history=conversation_history
    )
