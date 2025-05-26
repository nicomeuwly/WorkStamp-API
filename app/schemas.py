from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: str
    username: str
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class HourlyRateCreate(BaseModel):
    rate: float = Field(gt=0, description="Salaire horaire net en CHF")


class HourlyRateOut(BaseModel):
    id: int
    rate: float
    created_at: datetime

    class Config:
        from_attributes = True
