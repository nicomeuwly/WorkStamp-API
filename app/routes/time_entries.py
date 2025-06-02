from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from .. import schemas, crud, models
from ..dependencies import get_db
from ..utils.security import get_current_user
from datetime import date, datetime

router = APIRouter(prefix="/time-entries", tags=["working times"])


@router.post("", response_model=schemas.TimeEntryOut)
def add_time_entry(
    entry: schemas.TimeEntryCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return crud.create_time_entry(db, current_user.id, entry.start_time, entry.end_time)


@router.put("/{entry_id}", response_model=schemas.TimeEntryOut)
def edit_time_entry(
    entry_id: UUID,
    update: schemas.TimeEntryUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return crud.update_time_entry(db, entry_id, current_user.id, update)


@router.delete("/{entry_id}")
def delete_entry(
    entry_id: UUID,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    crud.delete_time_entry(db, entry_id, current_user.id)
    return {"detail": "Entrée supprimée"}


@router.get("/day/{date}", response_model=list[schemas.TimeEntryOut])
def get_entries_by_day(
    date: date,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return crud.get_entries_for_day(db, current_user.id, date)


@router.get("/summary/days", response_model=list[schemas.WorkedDaySummary])
def get_days_worked_summary(
    year: int = Query(datetime.now().year),
    month: int = Query(datetime.now().month),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return crud.get_worked_days_summary(db, current_user.id, year, month)


@router.get("/summary/month", response_model=schemas.MonthlySummary)
def get_monthly_summary(
    year: int = Query(datetime.now().year),
    month: int = Query(datetime.now().month),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return crud.get_monthly_summary(db, current_user.id, year, month)
