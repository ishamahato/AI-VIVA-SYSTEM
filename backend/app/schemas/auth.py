from typing import Literal

from pydantic import BaseModel, EmailStr, Field

Role = Literal["student", "faculty"]


class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)
    role: Role


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    role: Role


class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str

    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut
