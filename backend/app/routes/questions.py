"""Question bank: faculty create/update/delete, everyone can list."""
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.question import Question
from ..schemas.question import QuestionCreate, QuestionUpdate, QuestionOut
from ..security import get_current_user, require_faculty

router = APIRouter(prefix="/questions", tags=["questions"])


@router.get("", response_model=List[QuestionOut])
def list_questions(
    subject: Optional[str] = None,
    difficulty: Optional[str] = None,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    q = db.query(Question)
    if subject:
        q = q.filter(Question.subject == subject)
    if difficulty:
        q = q.filter(Question.difficulty == difficulty)
    return q.order_by(Question.created_at.desc()).all()


@router.get("/subjects", response_model=List[str])
def list_subjects(db: Session = Depends(get_db), user=Depends(get_current_user)):
    rows = db.query(Question.subject).distinct().all()
    return [r[0] for r in rows]


@router.post("", response_model=QuestionOut, status_code=201)
def create_question(
    payload: QuestionCreate,
    db: Session = Depends(get_db),
    faculty=Depends(require_faculty),
):
    question = Question(**payload.model_dump(), created_by=faculty.id)
    db.add(question)
    db.commit()
    db.refresh(question)
    return question


@router.put("/{question_id}", response_model=QuestionOut)
def update_question(
    question_id: int,
    payload: QuestionUpdate,
    db: Session = Depends(get_db),
    faculty=Depends(require_faculty),
):
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found.")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(question, field, value)
    db.commit()
    db.refresh(question)
    return question


@router.delete("/{question_id}", status_code=204)
def delete_question(
    question_id: int,
    db: Session = Depends(get_db),
    faculty=Depends(require_faculty),
):
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found.")
    db.delete(question)
    db.commit()
    return None
