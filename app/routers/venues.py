from sqlalchemy.orm import Session
from ..db import get_db
from .. import schemas, models
from fastapi import APIRouter, HTTPException, Depends
from typing import List


router = APIRouter(
    prefix="/venues",
    tags=["venues"],
)


@router.post("/", response_model=schemas.VenueCreate)
async def create_venue(venue: schemas.VenueCreate, db: Session = Depends(get_db)):
    try:
        db_venue = models.Venue(name=venue.name, location=venue.location, capacity=venue.capacity, venue_type=venue.venue_type)
        db.add(db_venue)
        db.commit()
        db.refresh(db_venue)
        return db_venue
    except:
        raise HTTPException(status_code=400, detail="Error creating venue")


@router.get("/", response_model=List[schemas.Venue])
async def read_venues(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    venues = db.query(models.Venue).offset(skip).limit(limit).all()
    return venues


@router.get("/{venue_id}", response_model=schemas.Venue)
async def read_venue(venue_id: int, db: Session = Depends(get_db)):
    venue = db.query(models.Venue).filter(models.Venue.id == venue_id).first()
    if venue is None:
        raise HTTPException(status_code=404, detail="Venue not found")
    return venue


@router.post("/{venue_id}/book", response_model=schemas.VenueBooking)
async def book_venue(venue_id: int, venue_booking: schemas.VenueBookingCreate, db: Session = Depends(get_db)):
    permission = db.query(models.Permission).filter(models.Permission.id == venue_booking.permission_id).first()
    if permission is None:
        raise HTTPException(status_code=404, detail="Permission not found")
    if permission.status != "approved":
        raise HTTPException(status_code=400, detail="Permission not approved")
    if permission.permission_type != "venue":
        raise HTTPException(status_code=400, detail="Invalid permission")
    db_venue_booking = models.VenueBooking(venue_id=venue_id, event_id=venue_booking.event_id, start_time=venue_booking.start_time, end_time=venue_booking.end_time, purpose=venue_booking.purpose, booker_id=venue_booking.booker_id)
    db.add(db_venue_booking)
    db.commit()
    db.refresh(db_venue_booking)
    return db_venue_booking
