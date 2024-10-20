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
async def create_event(event: schemas.EventCreate, db: Session = Depends(get_db)):

    db_event = models.Event(title=event.title, description=event.description, start_date=event.start_date, end_date=event.end_date, organizer_id=1, expected_attendance=event.expected_attendance)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event




@router.get("/", response_model=List[schemas.Event])
async def read_events(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), search: str = None):
    if search is not None:
        events = db.query(models.Event).filter(func.lower(models.Event.title).contains(search.lower())).offset(skip).limit(limit).all()
    else:
        events = db.query(models.Event).offset(skip).limit(limit).all()
    return events


@router.get("/{event_id}", response_model=schemas.EventOut)
async def read_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@router.post("/{event_id}/book", response_model=schemas.VenueBooking)
async def book_venue(event_id: int, venue_booking: schemas.VenueBookingCreate, db: Session = Depends(get_db)):
    db_venue_booking = models.VenueBooking(venue_id=venue_booking.venue_id, event_id=event_id, booker_id=venue_booking.booker_id, start_time=venue_booking.start_time, end_time=venue_booking.end_time, purpose=venue_booking.purpose)
    db.add(db_venue_booking)
    db.commit()
    db.refresh(db_venue_booking)
    return db_venue_booking



