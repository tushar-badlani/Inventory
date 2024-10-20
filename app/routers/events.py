from sqlalchemy import func
from sqlalchemy.orm import Session
from ..db import get_db
from .. import schemas, models, oauth2
from fastapi import APIRouter, HTTPException, Depends
from typing import List


router = APIRouter(
    prefix="/events",
    tags=["events"],
)


@router.post("/", response_model=schemas.EventCreate)
async def create_event(event: schemas.EventCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    if current_user.role == "student":
        raise HTTPException(status_code=401, detail="Not authorized")
    db_event = models.Event(title=event.title, description=event.description, start_date=event.start_date, end_date=event.end_date, expected_attendance=event.expected_attendance)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event




@router.get("/", response_model=List[schemas.Event])
async def read_events(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), search: str = None):
    if search is not None:
        events = db.query(models.Event).filter(func.lower(models.Event.title).contains(search.lower())).filter(models.Event.status == "approved").offset(skip).limit(limit).all()
    else:
        events = db.query(models.Event).offset(skip).limit(limit).all()
    return events


@router.get("/{event_id}", response_model=schemas.EventOut)
async def read_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@router.post("/{event_id}/approve", response_model=schemas.EventOut)
async def approve_event(event_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    if current_user.role == "student":
        raise HTTPException(status_code=401, detail="Not authorized")
    if current_user.role == "organization":
        raise HTTPException(status_code=401, detail="Not authorized")
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    event.status = "approved"
    db.commit()
    db.refresh(event)
    return event


@router.post("/{event_id}/reject", response_model=schemas.EventOut)
async def reject_event(event_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    if current_user.role == "student":
        raise HTTPException(status_code=401, detail="Not authorized")
    if current_user.role == "organization":
        raise HTTPException(status_code=401, detail="Not authorized")
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    event.status = "rejected"
    db.commit()
    db.refresh(event)
    return event


@router.post("/{event_id}/register", response_model=schemas.RegisterationOut)
async def register_event(event_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    db_registeration = models.Registeration(user_id=current_user.id, event_id=event_id)
    db.add(db_registeration)
    db.commit()
    db.refresh(db_registeration)
    return db_registeration


@router.delete("/{event_id}/register", response_model=schemas.RegisterationOut)
async def unregister_event(event_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    db_registeration = db.query(models.Registeration).filter(models.Registeration.user_id == current_user.id).filter(models.Registeration.event_id == event_id).first()
    if db_registeration is None:
        raise HTTPException(status_code=404, detail="User not registered for event")
    db.delete(db_registeration)
    db.commit()
    return db_registeration





