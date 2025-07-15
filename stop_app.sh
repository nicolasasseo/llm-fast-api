#!/bin/bash

# Kill all Uvicorn processes
pkill -f "uvicorn"
sudo pkill -f "uvicorn"

# Kill all Ollama processes
pkill -f "ollama"
sudo pkill -f "ollama"

echo "All Uvicorn and Ollama processes have been stopped." 