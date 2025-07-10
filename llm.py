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
    return os.getenv("OLLAMA_MODEL_NAME", "llama2")


def generate(
    prompt: str,
    max_tokens: int = 128,
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

    response = cast(
        Dict[str, Any],
        ollama.chat(
            model=_get_model_name(),
            messages=[{"role": "user", "content": prompt}],
            options=cast(Any, options),  # silences previous arg-type warning
            stream=False,  # returns a dict, not an iterator
        ),
    )

    # Ollama returns a dict with key 'message' containing 'content'
    return response["message"]["content"].strip()
