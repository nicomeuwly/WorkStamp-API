from sqlalchemy.orm import Session
from typing import Optional
from app.utils.auth import verify_password
from app.models import user as models


def authenticate_user(db: Session, username: str, password: str) -> Optional[models.User]:
    user = db.query(models.User).filter(models.User.username == username).first()
    if user and verify_password(password, str(user.hashed_password)):
        return user
    return None