from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from .base import Base
from .user import User
from .restaurant import Restaurant
from app.schemas.reservation import ReservationStatus

class Reservation(Base):
    __tablename__ = "reservations"
    
    id = Column(Integer, primary_key=True, index=True)
    date_time = Column(DateTime, nullable=False)
    party_size = Column(Integer, nullable=False)
    special_requests = Column(String(500), nullable=True)  # tamaño explícito
    status = Column(Enum(ReservationStatus), default=ReservationStatus.PENDING, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=False)
    
    # Relaciones
    user = relationship("User", back_populates="reservations")
    restaurant = relationship("Restaurant", back_populates="reservations")
