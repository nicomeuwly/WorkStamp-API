from sqlalchemy.orm import Session
from app.models import user as models
from app.schemas import user as schemas
from app.utils import auth


def create_user(db: Session, user: schemas.UserCreate):
    db_username = db.query(models.User).filter(
        models.User.username == user.username).first()
    db_email = db.query(models.User).filter(
        models.User.email == user.email).first()
    if db_username or db_email:
        return None
    hashed_password = auth.get_password_hash(user.password)
    new_user = models.User(username=user.username, email=user.email, first_name=user.first_name,
                           last_name=user.last_name, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user_by_username(db: Session, username: str):
    user = db.query(models.User).filter(
        models.User.username == username).first()
    if not user:
        return None
    return user


def get_current_user(token: str, db: Session):
    username = auth.verify_access_token(token)
    if username is None:
        return None
    user = get_user_by_username(db, username=username)
    if user is None:
        return None
    return user

def get_all_users(db: Session):
    users = db.query(models.User).all()
    if not users:
        return None
    return users

def is_superuser(user: models.User):
    if bool(user.is_superuser):
        return True
    return False