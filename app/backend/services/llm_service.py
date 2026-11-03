import os
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types

PROJECT_ROOT = Path(__file__).resolve().parents[3]

load_dotenv(PROJECT_ROOT / ".env")

MODEL_NAME = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.5-flash-lite"
)


@lru_cache(maxsize=1)
def get_gemini_client():
    """Create and reuse the Gemini API client."""

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured."
        )

    return genai.Client(api_key=api_key)


def generate_response(
    prompt: str,
    system_instruction: str
) -> str:
    """Generate text using the Gemini API."""

    client = get_gemini_client()

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.1,
            max_output_tokens=1024
        )
    )

    if not response.text:
        raise RuntimeError(
            "Gemini returned no text response."
        )

    return response.text.strip()
