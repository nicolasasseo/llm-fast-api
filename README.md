# Simple Chat API

A lightweight FastAPI application that provides a simple chat interface using [Ollama](https://ollama.ai) for local text generation. The application maintains conversation history in memory (as a list of message dicts) and now supports streaming responses.

## Features

- **Simple Chat Interface**: Send messages and get LLM responses
- **In-Memory History**: Maintains conversation history as a list of message dicts (`role`/`content`)
- **System Prompt Support**: Define agent behavior with system prompts
- **Local AI Generation**: Powered by Ollama (works on CPU, GPU acceleration optional)
- **Streaming Support**: Stream LLM responses as they are generated
- **Interactive Documentation**: Auto-generated Swagger UI

## API Endpoints

- `POST /chat` - Send a message and get AI response with conversation history
- `POST /chat/stream` - Stream the AI response as it is generated
- `GET /history` - Get the full conversation history
- `DELETE /history` - Clear the conversation history

## Requirements

- Python 3.10+
- (Optional) NVIDIA GPU for faster inference

## Installation

1. **Install Python dependencies:**

```bash
pip install -r requirements.txt
```

2. **Install and start Ollama:**

```bash
# Install Ollama
curl https://ollama.ai/install.sh | sh

# Start the Ollama daemon
ollama serve

# Pull a model (in another terminal)
ollama pull llama2
```

**Note on GPU Usage**: Ollama automatically detects and uses available NVIDIA GPUs for faster inference. If no GPU is available, it will run on CPU. No additional configuration is needed.

## Environment Variables

Create a `.env` file with the following variables:

```env
# Ollama model name (defaults to llama2)
OLLAMA_MODEL_NAME=llama2
```

## Running the Application

1. **Start the Ollama daemon** (if not already running):

```bash
ollama serve
```

2. **Run the FastAPI application:**

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

3. **Access the API:**

- Interactive documentation: `http://127.0.0.1:8000/docs`
- API base URL: `http://127.0.0.1:8000`

## Usage Examples

### 1. **Send a message (standard response):**

```bash
curl -X POST "http://127.0.0.1:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello, how are you?",
    "system_prompt": "You are a helpful assistant."
  }'
```

### 2. **Stream a response:**

```bash
curl -N -X POST "http://127.0.0.1:8000/chat/stream" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Tell me a story.",
    "system_prompt": "You are a creative storyteller."
  }'
```

### 3. **Get conversation history:**

```bash
curl "http://127.0.0.1:8000/history"
```

### 4. **Clear conversation history:**

```bash
curl -X DELETE "http://127.0.0.1:8000/history"
```

## Project Structure

```
chatapi/
├── main.py              # FastAPI application and routes
├── schemas.py           # Pydantic request/response schemas
├── llm.py               # Ollama integration (with streaming)
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

## Security Best Practices

- **Use HTTPS**: Deploy behind a reverse proxy (Nginx, Caddy) with SSL certificates.
- **Restrict Security Groups**: Only open necessary ports (e.g., 443 for HTTPS, 22 for SSH) and restrict to trusted IPs.
- **API Authentication**: Protect endpoints with API keys or JWTs in production.
- **Keep Software Updated**: Regularly update OS, Python, and dependencies.
- **Run as Non-Root**: Use a dedicated user for running the app.
- **Monitor and Log**: Set up logging and monitoring for suspicious activity.
- **Hide Docs in Production**: Remove or protect `/docs` and `/redoc` endpoints.

## Development Notes

- Conversation history is stored in memory as a list of message dicts (`{"role": ..., "content": ...}`) and is not persisted.
- Streaming is supported via `/chat/stream` and works best with clients that support chunked responses (e.g., curl, custom web clients).
- For production, consider using a persistent store for conversation history and implementing authentication.

## License

MIT
