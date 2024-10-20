from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Enum, Text, Float
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func
import enum

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    role = Column(String(50), nullable=False)
    department = Column(String(100))
    created_at = Column(DateTime, server_default=func.now())
    is_active = Column(Boolean, default=True)
    profile_pic = Column(String(255))

    # Relationships
    events_organized = relationship("Event", back_populates="organizer")
    inventory_requests = relationship("InventoryRequest", back_populates="requester")
    venue_bookings = relationship("VenueBooking",
                                back_populates="booker",
                                foreign_keys="VenueBooking.booker_id")
    permissions_to_approve = relationship("Permission",
                                       back_populates="approver",
                                       foreign_keys="Permission.approver_id")
    permissions_requested = relationship("Permission",
                                      back_populates="requestor",
                                      foreign_keys="Permission.user_id")

class Venue(Base):
    __tablename__ = 'venues'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    venue_type = Column(String(50), nullable=False)  # hall, classroom, lab
    capacity = Column(Integer)
    location = Column(String(100))
    is_active = Column(Boolean, default=True)
    picture = Column(String(255))

    # Relationships
    bookings = relationship("VenueBooking", back_populates="venue")

class VenueBooking(Base):
    __tablename__ = 'venue_bookings'

    id = Column(Integer, primary_key=True)
    venue_id = Column(Integer, ForeignKey('venues.id'))
    event_id = Column(Integer, ForeignKey('events.id'))
    permission_id = Column(Integer, ForeignKey('permissions.id'))
    booker_id = Column(Integer, ForeignKey('users.id'))  # Added missing foreign key
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    purpose = Column(Text)
    status = Column(String(50), default='approved')
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    venue = relationship("Venue", back_populates="bookings")
    event = relationship("Event", back_populates="venue_bookings")
    booker = relationship("User", back_populates="venue_bookings")  # Added relationship

class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    organizer_id = Column(Integer, ForeignKey('users.id'))
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    status = Column(String(50), default='draft')
    expected_attendance = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    type = Column(String(50))
    logo = Column(String(255))

    # Relationships
    organizer = relationship("User", back_populates="events_organized")
    venue_bookings = relationship("VenueBooking", back_populates="event")
    inventory_requests = relationship("InventoryRequest", back_populates="event")
    permissions = relationship("Permission", back_populates="event")

class InventoryItem(Base):
    __tablename__ = 'inventory_items'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    category = Column(String(50))  # event materials, marketing supplies, stationery
    quantity_available = Column(Integer, default=0)
    unit = Column(String(20))  # pieces, sets, boxes
    minimum_stock = Column(Integer, default=0)
    last_restocked = Column(DateTime)

    # Relationships
    requests = relationship("InventoryRequest", back_populates="item")
    transactions = relationship("InventoryTransaction", back_populates="item")

class InventoryRequest(Base):
    __tablename__ = 'inventory_requests'

    id = Column(Integer, primary_key=True)
    requester_id = Column(Integer, ForeignKey('users.id'))
    item_id = Column(Integer, ForeignKey('inventory_items.id'))
    event_id = Column(Integer, ForeignKey('events.id'))
    quantity_requested = Column(Integer, nullable=False)
    status = Column(String(50), default='pending')
    request_date = Column(DateTime, server_default=func.now())
    return_date = Column(DateTime)

    # Relationships
    requester = relationship("User", back_populates="inventory_requests")
    item = relationship("InventoryItem", back_populates="requests")
    event = relationship("Event", back_populates="inventory_requests")

class InventoryTransaction(Base):
    __tablename__ = 'inventory_transactions'

    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey('inventory_items.id'))
    quantity = Column(Integer, nullable=False)
    transaction_type = Column(String(20))  # in, out
    reference = Column(String(100))  # purchase order or request reference
    transaction_date = Column(DateTime, server_default=func.now())

    # Relationships
    item = relationship("InventoryItem", back_populates="transactions")

class Permission(Base):
    __tablename__ = 'permissions'

    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey('events.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    approver_id = Column(Integer, ForeignKey('users.id'))
    permission_type = Column(String(50))  # venue, budget, equipment
    status = Column(String(50), default='pending')
    description = Column(Text)
    requested_at = Column(DateTime, server_default=func.now())

    # Relationships
    event = relationship("Event", back_populates="permissions")
    approver = relationship("User",
                          back_populates="permissions_to_approve",
                          foreign_keys=[approver_id])
    requestor = relationship("User",
                           back_populates="permissions_requested",
                           foreign_keys=[user_id])

class Registration(Base):
    __tablename__ = 'registrations'

    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey('events.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    registration_date = Column(DateTime, server_default=func.now())

    # Relationships
    event = relationship("Event", back_populates="registrations")
    user = relationship("User", back_populates="registrations")