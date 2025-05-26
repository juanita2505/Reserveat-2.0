from sqlalchemy import Column, Integer, String, Time, ForeignKey, Enum
from sqlalchemy.orm import relationship
from .base import Base
from .user import User
from app.schemas.restaurant import CuisineType, PriceRange

class Restaurant(Base):
    __tablename__ = "restaurants"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True, nullable=False)           # tamaño obligatorio
    address = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=True)
    description = Column(String(500), nullable=True)
    cuisine_type = Column(Enum(CuisineType), nullable=False)
    price_range = Column(Enum(PriceRange), nullable=False)
    opening_time = Column(Time, nullable=False)
    closing_time = Column(Time, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relaciones
    owner = relationship("User", back_populates="restaurants")
    reservations = relationship("Reservation", back_populates="restaurant")
    
    def is_open_now(self):
        from datetime import datetime
        now = datetime.now().time()
        return self.opening_time <= now <= self.closing_time
