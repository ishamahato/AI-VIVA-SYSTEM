"""Read access to graded results."""
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.result import Result
from ..schemas.result import ResultOut
from ..security import get_current_user

router = APIRouter(prefix="/results", tags=["results"])


@router.get("/me", response_model=List[ResultOut])
def my_results(db: Session = Depends(get_db), user=Depends(get_current_user)):
    """A student's own history. Faculty get an empty list here (use dashboard)."""
    if user.role != "student":
        return []
    return (
        db.query(Result)
        .filter(Result.student_id == user.id)
        .order_by(Result.created_at.desc())
        .all()
    )


@router.get("/{result_id}", response_model=ResultOut)
def get_result(result_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    result = db.query(Result).filter(Result.id == result_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Result not found.")
    # students may only see their own results; faculty may see any
    if user.role == "student" and result.student_id != user.id:
        raise HTTPException(status_code=403, detail="Not allowed.")
    return result
