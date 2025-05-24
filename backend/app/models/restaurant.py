from sqlalchemy import Column, Integer, String, Time, ForeignKey, Enum
from sqlalchemy.orm import relationship
from .base import Base
from .user import User
from app.schemas.restaurant import CuisineType, PriceRange

class Restaurant(Base):
    __tablename__ = "restaurants"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    address = Column(String)
    phone = Column(String)
    description = Column(String)
    cuisine_type = Column(Enum(CuisineType))
    price_range = Column(Enum(PriceRange))
    opening_time = Column(Time)
    closing_time = Column(Time)
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    # Relaciones
    owner = relationship("User", back_populates="restaurants")
    reservations = relationship("Reservation", back_populates="restaurant")
    
    def is_open_now(self):
        from datetime import datetime
        now = datetime.now().time()
        return self.opening_time <= now <= self.closing_time