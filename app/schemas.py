from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, date
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
        model_config = {"from_attributes": True}


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

    class Config:
        from_attributes = True


class TimeEntryCreate(BaseModel):
    start_time: datetime
    end_time: Optional[datetime] = None


class TimeEntryUpdate(BaseModel):
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None


class TimeEntryOut(BaseModel):
    id: UUID
    start_time: datetime
    end_time: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class WorkedDaySummary(BaseModel):
    date: date
    total_hours: float
    entry_count: int


class MonthlySummary(BaseModel):
    month: str 
    total_days: int
    total_hours: float
    hourly_rate: float
    salary: float
