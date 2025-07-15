#!/bin/bash

# Kill all running Ollama processes
sudo pkill -f ollama

# Start Ollama in the background
ollama serve &

# Wait a few seconds to ensure Ollama is up
sleep 2

# Start your FastAPI app
uvicorn main:app --host 0.0.0.0 --port 8000
