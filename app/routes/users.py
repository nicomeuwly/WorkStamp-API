from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, crud, models
from ..dependencies import get_db
from ..utils.security import get_current_user
from ..models import User

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def register_user(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    # Vérifie si l'utilisateur existe déjà
    existing_user = db.query(models.User).filter(
        (models.User.username == user_data.username) | (models.User.email == user_data.email)).first()
    if existing_user:
        raise HTTPException(
            status_code=400, detail="Email ou nom d'utilisateur déjà utilisé.")

    return crud.create_user(db, user_data)


@router.get("/me", response_model=schemas.UserOut)
def read_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/hourly-rate", response_model=schemas.HourlyRateOut)
def add_hourly_rate(
    rate: schemas.HourlyRateCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return crud.create_hourly_rate(db, current_user.id, rate.rate, rate.effective_from)


@router.get("/hourly-rate", response_model=list[schemas.HourlyRateOut])
def get_hourly_rates(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    rates = crud.get_user_rates(db, current_user.id)
    if not rates:
        raise HTTPException(
            status_code=404, detail="Aucun taux horaire trouvé")
    return rates


@router.get("/hourly-rate/latest", response_model=schemas.HourlyRateOut)
def get_latest_rate(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    rate = crud.get_latest_hourly_rate(db, current_user.id)
    if not rate:
        raise HTTPException(
            status_code=404, detail="Aucun taux horaire trouvé")
    return rate
