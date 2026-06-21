"""Speech-to-text using Gemini multimodal `generate_content`.

The browser's MediaRecorder usually produces audio/webm (opus). We pass the
raw bytes inline. For very large files (>20 MB) the Files API would be needed,
but viva answers are short, so inline is fine.
"""
from google.genai import types

from ..gemini_client import get_client
from ...config import settings

_TRANSCRIBE_PROMPT = (
    "Transcribe this spoken answer to plain text exactly as said. "
    "The speaker may mix English and Nepali. Return ONLY the transcript text, "
    "with no labels, quotes, or extra commentary."
)


def transcribe_audio(audio_bytes: bytes, mime_type: str = "audio/webm") -> str:
    """Return the transcript for the given audio bytes."""
    client = get_client()
    response = client.models.generate_content(
        model=settings.GEMINI_MODEL,
        contents=[
            _TRANSCRIBE_PROMPT,
            types.Part.from_bytes(data=audio_bytes, mime_type=mime_type),
        ],
    )
    return (response.text or "").strip()
