from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Float, Time, Enum
from sqlalchemy.orm import relationship
from app.database import Base
from enum import Enum as PyEnum

class UserRole(str, PyEnum):
    CUSTOMER = "customer"
    RESTAURANT_OWNER = "restaurant_owner"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    phone_number = Column(String)
    role = Column(Enum(UserRole), default=UserRole.CUSTOMER)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default='now()')
    
    reservations = relationship("Reservation", back_populates="user")
    owned_restaurants = relationship("Restaurant", back_populates="owner")

class Restaurant(Base):
    __tablename__ = "restaurants"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String)
    address = Column(String, nullable=False)
    city = Column(String)
    postal_code = Column(String)
    cuisine_type = Column(String)
    opening_time = Column(Time)
    closing_time = Column(Time)
    capacity = Column(Integer)
    price_range = Column(Integer)  # 1-4 escalas de precio
    rating = Column(Float)
    owner_id = Column(Integer, ForeignKey("users.id"))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default='now()')
    
    reservations = relationship("Reservation", back_populates="restaurant")
    owner = relationship("User", back_populates="owned_restaurants")
    menu_items = relationship("MenuItem", back_populates="restaurant")

class ReservationStatus(str, PyEnum):
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    NO_SHOW = "no_show"

class Reservation(Base):
    __tablename__ = "reservations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    reservation_time = Column(DateTime, nullable=False)
    party_size = Column(Integer, nullable=False)
    status = Column(Enum(ReservationStatus), default=ReservationStatus.CONFIRMED)
    special_requests = Column(String)
    created_at = Column(DateTime, server_default='now()')
    
    user = relationship("User", back_populates="reservations")
    restaurant = relationship("Restaurant", back_populates="reservations")

class MenuItem(Base):
    __tablename__ = "menu_items"
    
    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    category = Column(String)
    is_available = Column(Boolean, default=True)
    
    restaurant = relationship("Restaurant", back_populates="menu_items")