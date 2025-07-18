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
# Ollama model name
OLLAMA_MODEL_NAME=<model>
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

## Project Structure

```
chatapi/
├── main.py              # FastAPI application and routes
├── schemas.py           # Pydantic request/response schemas
├── llm.py               # Ollama integration (with streaming)
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

## Production Deployment on AWS EC2 with Caddy

This section describes how to deploy the chat API on an AWS EC2 instance, set up a secure reverse proxy with Caddy, and configure DNS for a custom domain.

### 1. **Provision an EC2 Instance**

- Launch an Ubuntu EC2 instance with sufficient CPU/RAM (and GPU if needed).
- Open only necessary ports in the security group: 22 (SSH), 80 (HTTP), 443 (HTTPS).

### 2. **Install System Dependencies**

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv curl
```

### 3. **Install Ollama**

```bash
curl https://ollama.ai/install.sh | sh
ollama serve &  # Start Ollama in the background
```

### 4. **Clone the Project and Set Up Python**

```bash
git clone <your-repo-url> llm-fast-api
cd llm-fast-api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 5. **Pull the Required Ollama Model**

```bash
ollama pull <model-name>  # e.g., tinyllama:latest
```

### 6. **Set Up Environment Variables**

- Create a `.env` file in your project directory:
  ```env
  OLLAMA_MODEL_NAME=tinyllama:latest
  ```

### 7. **Run the FastAPI App**

```bash
./start_app.sh
```

### 8. **Install and Configure Caddy as a Reverse Proxy**

- Install Caddy:
  ```bash
  sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https
  curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo apt-key add -
  curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy-stable.list
  sudo apt update
  sudo apt install caddy
  ```
- Edit the Caddyfile (usually at `/etc/caddy/Caddyfile`):
  ```
  llm.wearegenial.com {
      reverse_proxy localhost:8000
  }
  ```
- Reload Caddy:
  ```bash
  sudo systemctl reload caddy
  ```

### 9. **Configure DNS with Route 53**

- Create an A record in your Route 53 hosted zone pointing `your_custom_domain_name.com` to your EC2 public IP.
- Wait for DNS propagation.

### 10. **Access Your API Securely**

- Visit `https://your_custom_domain_name.com` to access your API over HTTPS.
- Caddy will automatically obtain and renew SSL certificates.

### 11. **Troubleshooting Tips**

- If Caddy or FastAPI is not working, check logs:
  - `sudo journalctl -u caddy -f` (Caddy logs)
  - Your FastAPI terminal for errors
- If Ollama reports model not found, ensure you have pulled the correct model.
- If you get permission errors with `/etc/caddy/Caddyfile`, use `sudo` to view or edit it.
- Only ports 80/443 should be open to the public; port 8000 should not be exposed.

## Security Best Practices

- **Use HTTPS**: Deploy behind a reverse proxy (Caddy) with SSL certificates (Caddy automates this).
- **Restrict Security Groups**: Only open necessary ports (22 for SSH, 80/443 for HTTP/HTTPS) and restrict to trusted IPs when possible.
- **API Authentication**: Protect endpoints with API keys or JWTs in production.
- **Keep Software Updated**: Regularly update OS, Python, and dependencies.
- **Run as Non-Root**: Use a dedicated user for running the app and avoid running services as root.
- **Monitor and Log**: Set up logging and monitoring for suspicious activity (see Caddy and FastAPI logs).
- **Hide Docs in Production**: Remove or protect `/docs` and `/redoc` endpoints.
- **Do Not Expose Internal Ports**: Only expose ports 80/443 to the public; keep FastAPI (8000) internal.
- **Environment Variables**: Never commit `.env` files with secrets to version control; create/upload them manually on the server.

## Development Notes

- Conversation history is stored in memory as a list of message dicts (`{"role": ..., "content": ...}`) and is not persisted.
- Streaming is supported via `/chat/stream` and works best with clients that support chunked responses (e.g., curl, custom web clients).
- For production, consider using a persistent store for conversation history and implementing authentication.

## License

MIT
