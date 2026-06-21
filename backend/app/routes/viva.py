"""The viva flow: get questions, submit a spoken (or typed) answer, get graded."""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy import func
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.question import Question
from ..models.result import Result
from ..schemas.viva import (
    VivaStartRequest,
    VivaStartResponse,
    TextAnswerRequest,
    AnswerResult,
)
from ..security import require_student
from ..services.validation.answer_validator import validate_audio
from ..services.speech.gemini_speech import transcribe_audio
from ..services.evaluation.gemini_service import evaluate_answer
from ..services.gemini_client import GeminiNotConfigured

router = APIRouter(prefix="/viva", tags=["viva"])


def _grade_and_save(db: Session, student_id: int, question: Question, transcript: str) -> Result:
    """Run Gemini grading on a transcript and persist a Result row."""
    try:
        graded = evaluate_answer(
            question=question.text,
            expected_answer=question.expected_answer,
            keywords=question.keywords,
            transcript=transcript,
        )
    except GeminiNotConfigured as e:
        raise HTTPException(status_code=503, detail=str(e))

    result = Result(
        student_id=student_id,
        question_id=question.id,
        transcript=transcript,
        score=graded["score"],
        feedback=graded["feedback"],
        strengths=graded["strengths"],
        improvements=graded["improvements"],
    )
    db.add(result)
    db.commit()
    db.refresh(result)
    return result


@router.post("/start", response_model=VivaStartResponse)
def start_viva(
    payload: VivaStartRequest,
    db: Session = Depends(get_db),
    student=Depends(require_student),
):
    q = db.query(Question)
    if payload.subject:
        q = q.filter(Question.subject == payload.subject)
    if payload.difficulty:
        q = q.filter(Question.difficulty == payload.difficulty)

    questions = q.order_by(func.random()).limit(payload.num_questions).all()
    if not questions:
        raise HTTPException(status_code=404, detail="No questions match those filters.")
    return VivaStartResponse(questions=questions)


@router.post("/answer", response_model=AnswerResult)
async def submit_audio_answer(
    question_id: int = Form(...),
    audio: UploadFile = File(...),
    db: Session = Depends(get_db),
    student=Depends(require_student),
):
    """Submit a recorded answer: transcribe with Gemini, then grade it."""
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found.")

    raw = await audio.read()
    mime = validate_audio(audio.content_type, raw)

    try:
        transcript = transcribe_audio(raw, mime_type=mime)
    except GeminiNotConfigured as e:
        raise HTTPException(status_code=503, detail=str(e))

    result = _grade_and_save(db, student.id, question, transcript)
    return AnswerResult(
        result_id=result.id,
        question_id=question.id,
        transcript=result.transcript,
        score=result.score,
        feedback=result.feedback,
        strengths=result.strengths,
        improvements=result.improvements,
    )


@router.post("/answer-text", response_model=AnswerResult)
def submit_text_answer(
    payload: TextAnswerRequest,
    db: Session = Depends(get_db),
    student=Depends(require_student),
):
    """Submit a typed answer (useful for testing without a microphone)."""
    question = db.query(Question).filter(Question.id == payload.question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found.")

    result = _grade_and_save(db, student.id, question, payload.answer_text)
    return AnswerResult(
        result_id=result.id,
        question_id=question.id,
        transcript=result.transcript,
        score=result.score,
        feedback=result.feedback,
        strengths=result.strengths,
        improvements=result.improvements,
    )
