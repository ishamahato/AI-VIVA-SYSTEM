"""Manual / faculty-triggered re-evaluation of a stored answer."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.result import Result
from ..models.question import Question
from ..schemas.result import ResultOut
from ..security import require_faculty
from ..services.evaluation.gemini_service import evaluate_answer
from ..services.gemini_client import GeminiNotConfigured

router = APIRouter(prefix="/evaluation", tags=["evaluation"])


@router.post("/reevaluate/{result_id}", response_model=ResultOut)
def reevaluate(result_id: int, db: Session = Depends(get_db), faculty=Depends(require_faculty)):
    """Re-grade an existing answer's transcript (e.g. after editing the model answer)."""
    result = db.query(Result).filter(Result.id == result_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Result not found.")
    if not result.transcript:
        raise HTTPException(status_code=400, detail="This result has no transcript to grade.")

    question = db.query(Question).filter(Question.id == result.question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Original question no longer exists.")

    try:
        graded = evaluate_answer(
            question=question.text,
            expected_answer=question.expected_answer,
            keywords=question.keywords,
            transcript=result.transcript,
        )
    except GeminiNotConfigured as e:
        raise HTTPException(status_code=503, detail=str(e))

    result.score = graded["score"]
    result.feedback = graded["feedback"]
    result.strengths = graded["strengths"]
    result.improvements = graded["improvements"]
    db.commit()
    db.refresh(result)
    return result
