from uuid import UUID
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
import pytz


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: UUID
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
    effective_from: datetime = Field(
        default_factory=lambda: datetime.now(pytz.timezone("Europe/Paris")),
        description="Date à partir de laquelle le taux horaire est effectif",
    )


class HourlyRateOut(BaseModel):
    id: UUID
    rate: float
    effective_from: datetime
    created_at: datetime

    class Config:
        from_attributes = True
