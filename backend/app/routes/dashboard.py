"""Aggregated stats for the student and faculty dashboards."""
from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.result import Result
from ..models.question import Question
from ..models.student import Student
from ..schemas.dashboard import StudentDashboard, FacultyDashboard, SubjectStat
from ..security import require_student, require_faculty

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/student", response_model=StudentDashboard)
def student_dashboard(db: Session = Depends(get_db), student=Depends(require_student)):
    rows = (
        db.query(Result)
        .filter(Result.student_id == student.id)
        .order_by(Result.created_at.desc())
        .all()
    )
    scores = [r.score for r in rows if r.score is not None]
    total = len(rows)
    avg = round(sum(scores) / len(scores), 2) if scores else 0.0
    best = round(max(scores), 2) if scores else 0.0
    return StudentDashboard(
        total_vivas=total,
        average_score=avg,
        best_score=best,
        recent=rows[:5],
    )


@router.get("/faculty", response_model=FacultyDashboard)
def faculty_dashboard(db: Session = Depends(get_db), faculty=Depends(require_faculty)):
    total_questions = db.query(func.count(Question.id)).scalar() or 0
    total_students = db.query(func.count(Student.id)).scalar() or 0
    total_attempts = db.query(func.count(Result.id)).scalar() or 0

    avg_all = db.query(func.avg(Result.score)).scalar()
    average_score = round(float(avg_all), 2) if avg_all is not None else 0.0

    # per-subject breakdown (join results -> questions)
    subject_rows = (
        db.query(
            Question.subject,
            func.count(Result.id),
            func.avg(Result.score),
        )
        .join(Result, Result.question_id == Question.id)
        .group_by(Question.subject)
        .all()
    )
    by_subject = [
        SubjectStat(
            subject=subj,
            attempts=count,
            average_score=round(float(avg), 2) if avg is not None else 0.0,
        )
        for subj, count, avg in subject_rows
    ]

    return FacultyDashboard(
        total_questions=total_questions,
        total_students=total_students,
        total_attempts=total_attempts,
        average_score=average_score,
        by_subject=by_subject,
    )
