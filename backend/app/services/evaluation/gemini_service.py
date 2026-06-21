"""Grade a student's answer with Gemini and return a structured result.

Returns a dict:
    {
        "score": float (0-10),
        "feedback": str,
        "strengths": str,
        "improvements": str,
    }
"""
import json

from google.genai import types

from ..gemini_client import get_client
from ...config import settings


# Structured-output schema so Gemini returns clean JSON
_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "score": {"type": "number", "description": "Score from 0 to 10"},
        "feedback": {"type": "string", "description": "2-4 sentence overall feedback"},
        "strengths": {"type": "string", "description": "What the student did well"},
        "improvements": {"type": "string", "description": "What to improve"},
    },
    "required": ["score", "feedback", "strengths", "improvements"],
}


def _build_prompt(question: str, expected_answer: str | None, keywords: str | None,
                  transcript: str) -> str:
    reference = expected_answer.strip() if expected_answer else "(no model answer provided)"
    kw = keywords.strip() if keywords else "(none)"
    return (
        "You are a fair but rigorous university examiner grading a spoken viva answer.\n\n"
        f"QUESTION:\n{question}\n\n"
        f"MODEL ANSWER / KEY POINTS:\n{reference}\n\n"
        f"IMPORTANT KEYWORDS:\n{kw}\n\n"
        f"STUDENT'S SPOKEN ANSWER (transcribed):\n{transcript}\n\n"
        "Grade the student's answer for correctness, completeness, and clarity. "
        "Be encouraging but honest. Give a score from 0 to 10 (decimals allowed). "
        "Do not penalise minor transcription errors or filler words."
    )


def evaluate_answer(question: str, expected_answer: str | None, keywords: str | None,
                    transcript: str) -> dict:
    """Call Gemini and return a normalized evaluation dict."""
    client = get_client()

    if not transcript.strip():
        return {
            "score": 0.0,
            "feedback": "No answer was detected. Please try recording again.",
            "strengths": "",
            "improvements": "Provide a spoken answer to the question.",
        }

    response = client.models.generate_content(
        model=settings.GEMINI_MODEL,
        contents=_build_prompt(question, expected_answer, keywords, transcript),
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=_RESPONSE_SCHEMA,
            temperature=0.2,
        ),
    )

    data = json.loads(response.text)

    # normalize / clamp
    try:
        score = float(data.get("score", 0))
    except (TypeError, ValueError):
        score = 0.0
    score = max(0.0, min(10.0, score))

    return {
        "score": round(score, 2),
        "feedback": str(data.get("feedback", "")).strip(),
        "strengths": str(data.get("strengths", "")).strip(),
        "improvements": str(data.get("improvements", "")).strip(),
    }
