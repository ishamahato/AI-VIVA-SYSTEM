"""Password hashing, JWT creation/verification, and auth dependencies."""
from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from .config import settings
from .database import get_db
from .models.student import Student
from .models.faculty import Faculty

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# tokenUrl is only used by the interactive docs "Authorize" button
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


# ---------- passwords ----------
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


# ---------- tokens ----------
def create_access_token(user_id: int, role: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": str(user_id), "role": role, "exp": expire}
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


_credentials_exc = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Decode the JWT and return the matching Student or Faculty instance."""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        user_id = payload.get("sub")
        role = payload.get("role")
        if user_id is None or role is None:
            raise _credentials_exc
    except JWTError:
        raise _credentials_exc

    model = Student if role == "student" else Faculty
    user = db.query(model).filter(model.id == int(user_id)).first()
    if user is None:
        raise _credentials_exc
    return user


def require_student(user=Depends(get_current_user)):
    if user.role != "student":
        raise HTTPException(status_code=403, detail="Students only")
    return user


def require_faculty(user=Depends(get_current_user)):
    if user.role != "faculty":
        raise HTTPException(status_code=403, detail="Faculty only")
    return user
