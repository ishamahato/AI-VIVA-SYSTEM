"""Authentication: register, login, and current-user lookup."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.student import Student
from ..models.faculty import Faculty
from ..schemas.auth import RegisterRequest, LoginRequest, TokenResponse, UserOut
from ..security import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user,
)

router = APIRouter(prefix="/auth", tags=["auth"])


def _model_for(role: str):
    return Student if role == "student" else Faculty


@router.post("/register", response_model=TokenResponse, status_code=201)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    Model = _model_for(payload.role)

    # email must be unique across BOTH tables
    if (
        db.query(Student).filter(Student.email == payload.email).first()
        or db.query(Faculty).filter(Faculty.email == payload.email).first()
    ):
        raise HTTPException(status_code=409, detail="Email already registered.")

    user = Model(
        name=payload.name,
        email=payload.email,
        password_hash=hash_password(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token(user.id, payload.role)
    return TokenResponse(access_token=token, user=UserOut.model_validate(user))


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    Model = _model_for(payload.role)
    user = db.query(Model).filter(Model.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password.")

    token = create_access_token(user.id, payload.role)
    return TokenResponse(access_token=token, user=UserOut.model_validate(user))


@router.get("/me", response_model=UserOut)
def me(user=Depends(get_current_user)):
    return UserOut.model_validate(user)
