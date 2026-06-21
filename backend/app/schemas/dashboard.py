from typing import List

from pydantic import BaseModel

from .result import ResultOut


class StudentDashboard(BaseModel):
    total_vivas: int
    average_score: float
    best_score: float
    recent: List[ResultOut]


class SubjectStat(BaseModel):
    subject: str
    attempts: int
    average_score: float


class FacultyDashboard(BaseModel):
    total_questions: int
    total_students: int
    total_attempts: int
    average_score: float
    by_subject: List[SubjectStat]
