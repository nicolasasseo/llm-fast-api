#!/bin/bash

# Kill all running Ollama processes & FastAPI
pkill -f ollama
pkill -f uvicorn

# Start Ollama in the background, log output
ollama serve > ollama.log 2>&1 &

# Wait a few seconds to ensure Ollama is up
sleep 3

# Activate virtual environment and start FastAPI in the background, log output
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000 > fastapi.log 2>&1 &