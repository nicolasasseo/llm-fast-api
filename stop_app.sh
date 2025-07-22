#!/bin/bash

# Kill all Uvicorn processes
pkill -f "uvicorn"
sudo pkill -f "uvicorn"

# Kill all Ollama processes
pkill -f "ollama"
sudo pkill -f "ollama"

for LOGFILE in fastapi.log ollama.log; do
    if [ -f "$LOGFILE" ]; then
        if [ -s "$LOGFILE" ]; then
            cp "$LOGFILE" "old$LOGFILE"
        fi
        > "$LOGFILE"
    fi
done


echo "All Uvicorn and Ollama processes have been stopped." 