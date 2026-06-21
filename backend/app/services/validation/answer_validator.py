"""Lightweight validation for uploaded audio answers."""
from fastapi import HTTPException

# 20 MB inline limit for Gemini; viva answers are far smaller.
MAX_AUDIO_BYTES = 20 * 1024 * 1024

ALLOWED_AUDIO_PREFIXES = ("audio/",)


def validate_audio(content_type: str | None, data: bytes) -> str:
    """Validate the uploaded audio and return a usable mime type."""
    if not data:
        raise HTTPException(status_code=400, detail="Empty audio file.")
    if len(data) > MAX_AUDIO_BYTES:
        raise HTTPException(status_code=413, detail="Audio file too large (max 20 MB).")

    mime = (content_type or "").split(";")[0].strip().lower()
    if not mime or not mime.startswith(ALLOWED_AUDIO_PREFIXES):
        # Browser MediaRecorder default; safe fallback
        mime = "audio/webm"
    return mime
