from typing import List, Optional

from pydantic import BaseModel, Field

from .question import QuestionForViva


class VivaStartRequest(BaseModel):
    subject: Optional[str] = None
    difficulty: Optional[str] = None
    num_questions: int = Field(default=5, ge=1, le=20)


class VivaStartResponse(BaseModel):
    questions: List[QuestionForViva]


# For submitting an answer as plain text (testing without a microphone)
class TextAnswerRequest(BaseModel):
    question_id: int
    answer_text: str = Field(min_length=1)


class AnswerResult(BaseModel):
    result_id: int
    question_id: int
    transcript: str
    score: float
    feedback: str
    strengths: Optional[str] = None
    improvements: Optional[str] = None
