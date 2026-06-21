"""Shared Google GenAI (Gemini) client.

Uses the current `google-genai` SDK:
    from google import genai
    client = genai.Client(api_key=...)
    client.models.generate_content(model=..., contents=[...])

The legacy `google-generativeai` package is deprecated and is NOT used here.
"""
from functools import lru_cache

from google import genai

from ..config import settings


class GeminiNotConfigured(RuntimeError):
    """Raised when GEMINI_API_KEY is missing."""


@lru_cache(maxsize=1)
def get_client() -> genai.Client:
    if not settings.GEMINI_API_KEY:
        raise GeminiNotConfigured(
            "GEMINI_API_KEY is not set. Add it to backend/.env to enable AI features."
        )
    return genai.Client(api_key=settings.GEMINI_API_KEY)