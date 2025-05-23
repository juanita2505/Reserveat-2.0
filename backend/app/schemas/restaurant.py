from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import time
from .user import User

class CuisineType(str, Enum):
    MEXICAN = "mexican"
    ITALIAN = "italian"
    JAPANESE = "japanese"
    AMERICAN = "american"
    VEGETARIAN = "vegetarian"
    OTHER = "other"

class PriceRange(str, Enum):
    LOW = "$"
    MEDIUM = "$$"
    HIGH = "$$$"

class RestaurantBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    address: str = Field(..., min_length=5, max_length=200)
    phone: str = Field(..., min_length=10, max_length=15)
    description: Optional[str] = Field(None, max_length=500)
    cuisine_type: CuisineType
    price_range: PriceRange
    opening_time: time
    closing_time: time

class RestaurantCreate(RestaurantBase):
    pass

class RestaurantUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    address: Optional[str] = Field(None, min_length=5, max_length=200)
    phone: Optional[str] = Field(None, min_length=10, max_length=15)
    description: Optional[str] = Field(None, max_length=500)
    cuisine_type: Optional[CuisineType] = None
    price_range: Optional[PriceRange] = None
    opening_time: Optional[time] = None
    closing_time: Optional[time] = None

class Restaurant(RestaurantBase):
    id: int
    owner_id: int
    owner: User

    class Config:
        orm_mode = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Fine Dining",
                "address": "123 Main St",
                "phone": "+1234567890",
                "description": "A fine dining experience",
                "cuisine_type": "italian",
                "price_range": "$$$",
                "opening_time": "09:00:00",
                "closing_time": "23:00:00",
                "owner_id": 1
            }
        }

class RestaurantSearchResults(BaseModel):
    results: List[Restaurant]
    total: int