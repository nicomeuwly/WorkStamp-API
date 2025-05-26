from typing import Optional
from sqlalchemy.orm import Session
from . import models, schemas
from .utils.security import hash_password, verify_password
from datetime import datetime
import pytz


def create_user(db: Session, user_data: schemas.UserCreate) -> models.User:
    hashed_password = hash_password(user_data.password)
    user = models.User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hashed_password,
        created_at=datetime.now(pytz.timezone("Europe/Paris"))
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


def create_hourly_rate(db: Session, user_id: int, rate: float) -> models.HourlyRate:
    rate = models.HourlyRate(user_id=user_id, rate=rate)
    db.add(rate)
    db.commit()
    db.refresh(rate)
    return rate


def get_user_rates(db: Session, user_id: int) -> list[models.HourlyRate]:
    return db.query(models.HourlyRate)\
        .filter(models.HourlyRate.user_id == user_id)\
        .order_by(models.HourlyRate.created_at.desc())\
        .all()


def get_latest_hourly_rate(db: Session, user_id: int) -> Optional[models.HourlyRate]:
    return db.query(models.HourlyRate)\
        .filter(models.HourlyRate.user_id == user_id)\
        .order_by(models.HourlyRate.created_at.desc())\
        .first()
