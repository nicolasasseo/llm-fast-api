"""Utility module to interface with an Ollama server for text generation.

Requires the `ollama` Python client (pip install ollama) and a running
Ollama daemon on the host (typically listening at http://localhost:11434).
"""

from __future__ import annotations
from dotenv import load_dotenv
import os
from functools import lru_cache
from typing import Any, Dict, cast

load_dotenv()
import ollama


@lru_cache(maxsize=1)
def _get_model_name() -> str:
    """Return the model name configured via environment variable or default."""
    return os.getenv("OLLAMA_MODEL_NAME", "mistral:latest")


def generate(
    messages: list,
    max_tokens: int = -1,
    temperature: float = 0.7,
) -> str:
    """Generate text using the Ollama chat API.

    Parameters
    ----------
    prompt: str
        User prompt to send to the model.
    max_tokens: int
        Maximum tokens to generate (mapped to Ollama's `num_predict`).
    temperature: float
        Sampling temperature.
    """

    options: Dict[str, Any] = {
        "temperature": temperature,
        "num_predict": max_tokens,
    }

    print(_get_model_name())

    response = cast(
        Dict[str, Any],
        ollama.chat(
            model=_get_model_name(),
            messages=messages,
            options=cast(Any, options),  # silences previous arg-type warning
            stream=False,  # returns a dict, not an iterator
        ),
    )

    # Ollama returns a dict with key 'message' containing 'content'
    return response["message"]["content"].strip()


def generate_stream(
    messages: list,
    max_tokens: int = -1,
    temperature: float = 0.7,
):
    """Stream text using the Ollama chat API."""
    options: Dict[str, Any] = {
        "temperature": temperature,
        "num_predict": max_tokens,
    }

    print(_get_model_name())

    # This will yield each chunk as it is produced by the model
    for chunk in ollama.chat(
        model=_get_model_name(),
        messages=messages,
        options=cast(Any, options),
        stream=True,  # Enable streaming
    ):
        if isinstance(chunk, dict):
            content = chunk.get("message", {}).get("content", "")
            if content:
                yield content
        elif isinstance(chunk, str):
            yield chunk
