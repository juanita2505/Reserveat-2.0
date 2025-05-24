from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from .base import Base
from .user import User
from .restaurant import Restaurant
from app.schemas.reservation import ReservationStatus

class Reservation(Base):
    __tablename__ = "reservations"
    
    id = Column(Integer, primary_key=True, index=True)
    date_time = Column(DateTime)
    party_size = Column(Integer)
    special_requests = Column(String, nullable=True)
    status = Column(Enum(ReservationStatus), default=ReservationStatus.PENDING)
    user_id = Column(Integer, ForeignKey("users.id"))
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    
    # Relaciones
    user = relationship("User", back_populates="reservations")
    restaurant = relationship("Restaurant", back_populates="reservations")