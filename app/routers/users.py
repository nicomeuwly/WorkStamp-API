from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas import user as schemas
from app.dependencies.db import get_db
from app.crud import user as crud
from app.dependencies.auth import get_current_user_safe

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}}
)


@router.post("/register", response_model=schemas.User, status_code=201)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = crud.create_user(db, user)
    if new_user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already used"
        )
    return schemas.User.model_validate(new_user)


@router.get("/me", response_model=schemas.User)
def read_users_me(current_user=Depends(get_current_user_safe)):
    return schemas.User.model_validate(current_user)


@router.get("", response_model=list[schemas.User])
def read_all_users(current_user=Depends(get_current_user_safe), db: Session = Depends(get_db)):
    if not crud.is_superuser(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource"
        )
    users = crud.get_all_users(db)
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No users found"
        )
    return [schemas.User.model_validate(user) for user in users]
