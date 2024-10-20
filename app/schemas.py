from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str
    full_name: str
    role: str
    department: Optional[str] = None


class User(UserBase):
    id: int
    full_name: str
    role: str
    department: Optional[str] = None
    created_at: datetime
    is_active: bool




class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None
    role: Optional[str] = None



class VenueBase(BaseModel):
    name: str
    venue_type: str
    capacity: int
    location: str


class VenueCreate(VenueBase):
    pass


class Venue(VenueBase):
    id: int
    is_active: bool




class VenueBookingBase(BaseModel):
    venue_id: int
    event_id: int
    start_time: datetime
    end_time: datetime
    purpose: str



class VenueBookingCreate(VenueBookingBase):
    permission_id: int
    pass



class VenueBooking(VenueBookingBase):
    id: int
    status: str
    created_at: datetime



class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_date: datetime
    end_date: datetime
    type: Optional[str] = None
    logo: Optional[str] = None



class EventCreate(EventBase):
    expected_attendance: Optional[int] = None
    pass


class Event(EventBase):
    id: int
    organizer: User


class InventoryRequestBase(BaseModel):
    item_name: str
    quantity: int
    requestor_id: int


class InventoryRequestCreate(InventoryRequestBase):
    pass


class InventoryRequest(InventoryRequestBase):
    id: int
    status: str
    created_at: datetime



class PermissionBase(BaseModel):
    event_id: int
    approver_id: int
    permission_type: str
    description: Optional[str] = None


class PermissionCreate(PermissionBase):
    pass

class Permission(PermissionBase):
    id: int
    status: str
    created_at: Optional[datetime] = None



class Registeration(BaseModel):
    id: int
    event: Event
    user: User
    registration_date: datetime





class EventOut(Event):
    venue_bookings: List[VenueBooking] = []
    permissions: List[Permission] = []
    registerations: List[RegisterationOut] = []


class PermissionOut(Permission):
    requestor: User
    event: Event
    approver: User

class VenueOut(Venue):
    bookings: List[VenueBooking] = []


class VenueBookingOut(VenueBooking):
    venue: Venue
    event: Event
    booker: User


class UserOut(User):
    events_organized: List[Event] = []
    inventory_requests: List[InventoryRequest] = []
    venue_bookings: List[VenueBooking] = []
    permissions_to_approve: List[Permission] = []
    permissions_requested: List[Permission] = []
    registerations: List[RegisterationOut] = []

