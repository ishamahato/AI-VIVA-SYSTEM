from typing import Optional

from pydantic import BaseModel, Field


class QuestionBase(BaseModel):
    subject: str = Field(min_length=1, max_length=120)
    text: str = Field(min_length=1)
    difficulty: str = "medium"
    expected_answer: Optional[str] = None
    keywords: Optional[str] = None


class QuestionCreate(QuestionBase):
    pass


class QuestionUpdate(BaseModel):
    subject: Optional[str] = None
    text: Optional[str] = None
    difficulty: Optional[str] = None
    expected_answer: Optional[str] = None
    keywords: Optional[str] = None


class QuestionOut(QuestionBase):
    id: int
    created_by: Optional[int] = None

    model_config = {"from_attributes": True}


# Version sent to students during a viva (hides the model answer)
class QuestionForViva(BaseModel):
    id: int
    subject: str
    text: str
    difficulty: str

    model_config = {"from_attributes": True}
