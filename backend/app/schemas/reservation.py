from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from .user import User
from .restaurant import Restaurant

class ReservationStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"

class ReservationBase(BaseModel):
    restaurant_id: int
    date_time: datetime
    party_size: int = Field(..., gt=0, le=20)
    special_requests: Optional[str] = Field(None, max_length=500)

class ReservationCreate(ReservationBase):
    pass

class ReservationUpdate(BaseModel):
    date_time: Optional[datetime] = None
    party_size: Optional[int] = Field(None, gt=0, le=20)
    special_requests: Optional[str] = Field(None, max_length=500)
    status: Optional[ReservationStatus] = None

class Reservation(ReservationBase):
    id: int
    user_id: int
    status: ReservationStatus
    created_at: datetime
    updated_at: datetime
    user: User
    restaurant: Restaurant

    class Config:
        orm_mode = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "restaurant_id": 1,
                "user_id": 1,
                "date_time": "2023-12-31T20:00:00",
                "party_size": 4,
                "special_requests": "Window seat please",
                "status": "confirmed",
                "created_at": "2023-01-01T00:00:00",
                "updated_at": "2023-01-01T00:00:00"
            }
        }