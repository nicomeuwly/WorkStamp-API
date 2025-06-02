from typing import Optional
from uuid import UUID
from fastapi import HTTPException
from sqlalchemy import extract
from sqlalchemy.orm import Session
from . import models, schemas
from .utils.security import hash_password, verify_password
from datetime import datetime
from collections import defaultdict


def create_user(db: Session, user_data: schemas.UserCreate) -> models.User:
    hashed_password = hash_password(user_data.password)
    user = models.User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hashed_password
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str) -> Optional[models.User]:
    user = db.query(models.User).filter(models.User.email == email).first()
    if user and verify_password(password, user.password_hash):
        return user
    return None


def create_hourly_rate(db: Session, user_id: UUID, rate: float, effective_from: datetime) -> models.HourlyRate:
    rate = models.HourlyRate(user_id=user_id, rate=rate,
                             effective_from=effective_from,)
    db.add(rate)
    db.commit()
    db.refresh(rate)
    return rate


def get_user_rates(db: Session, user_id: UUID) -> list[models.HourlyRate]:
    return db.query(models.HourlyRate)\
        .filter(models.HourlyRate.user_id == user_id)\
        .order_by(models.HourlyRate.created_at.desc())\
        .all()


def get_latest_hourly_rate(db: Session, user_id: UUID) -> Optional[models.HourlyRate]:
    return db.query(models.HourlyRate)\
        .filter(models.HourlyRate.user_id == user_id)\
        .order_by(models.HourlyRate.created_at.desc())\
        .first()


def create_time_entry(db: Session, user_id: UUID, start: datetime, end: Optional[datetime]) -> models.TimeEntry:
    entry = models.TimeEntry(
        user_id=user_id,
        start_time=start,
        end_time=end
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


def update_time_entry(db: Session, entry_id: UUID, user_id: UUID, update: schemas.TimeEntryUpdate) -> models.TimeEntry:
    entry = db.query(models.TimeEntry).filter_by(
        id=str(entry_id), user_id=user_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Entrée introuvable")
    if update.start_time:
        entry.start_time = update.start_time
    if update.end_time is not None:
        entry.end_time = update.end_time
    db.commit()
    db.refresh(entry)
    return entry


def delete_time_entry(db: Session, entry_id: UUID, user_id: UUID):
    entry = db.query(models.TimeEntry).filter_by(
        id=str(entry_id), user_id=user_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Entrée introuvable")
    db.delete(entry)
    db.commit()


def get_entries_for_day(db: Session, user_id: UUID, date: datetime.date) -> list[models.TimeEntry]:
    start = datetime.combine(date, datetime.min.time())
    end = datetime.combine(date, datetime.max.time())
    return db.query(models.TimeEntry).filter(
        models.TimeEntry.user_id == user_id,
        models.TimeEntry.start_time >= start,
        models.TimeEntry.start_time <= end
    ).order_by(models.TimeEntry.start_time).all()


def get_worked_days_summary(db: Session, user_id: UUID, year: int, month:int) -> list[dict]:
    entries = db.query(models.TimeEntry).filter(
        models.TimeEntry.user_id == user_id,
        extract("year", models.TimeEntry.start_time) == year,
        extract("month", models.TimeEntry.start_time) == month,
        models.TimeEntry.end_time.isnot(None)
    ).all()

    summary = defaultdict(lambda: {"entry_count": 0, "total_hours": 0.0})

    for entry in entries:
        day = entry.start_time.date()
        duration = (entry.end_time - entry.start_time).total_seconds() / 3600
        summary[day]["entry_count"] += 1
        summary[day]["total_hours"] += duration

    result = [
        {
            "date": day,
            "entry_count": data["entry_count"],
            "total_hours": round(data["total_hours"], 2)
        }
        for day, data in sorted(summary.items())
    ]

    return result


def get_monthly_summary(db: Session, user_id: UUID, year: int, month: int) -> dict:
    start_of_month = datetime(year, month, 1)

    if month == 12:
        start_of_next_month = datetime(year + 1, 1, 1)
    else:
        start_of_next_month = datetime(year, month + 1, 1)

    entries = db.query(models.TimeEntry).filter(
        models.TimeEntry.user_id == user_id,
        models.TimeEntry.end_time.isnot(None),
        models.TimeEntry.start_time >= start_of_month,
        models.TimeEntry.start_time < start_of_next_month
    ).all()

    total_hours = sum(
        (entry.end_time - entry.start_time).total_seconds() / 3600
        for entry in entries
    )
    print(start_of_month)
    hourly_rate = db.query(models.HourlyRate).filter(
        models.HourlyRate.user_id == user_id,
        models.HourlyRate.effective_from <= start_of_month
    ).order_by(models.HourlyRate.effective_from.desc()).first()

    rate_amount = float(hourly_rate.rate) if hourly_rate else 0.0
    salary = round(total_hours * rate_amount, 2)

    return {
        "month": f"{year}-{month:02}",
        "total_days": len(set(entry.start_time.date() for entry in entries)),
        "total_hours": round(total_hours, 2),
        "hourly_rate": rate_amount,
        "salary": salary
    }
