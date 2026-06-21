from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from .question import QuestionForViva


class ResultOut(BaseModel):
    id: int
    student_id: int
    question_id: Optional[int] = None
    transcript: Optional[str] = None
    score: Optional[float] = None
    feedback: Optional[str] = None
    strengths: Optional[str] = None
    improvements: Optional[str] = None
    created_at: datetime
    question: Optional[QuestionForViva] = None

    model_config = {"from_attributes": True}
