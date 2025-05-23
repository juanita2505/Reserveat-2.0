from pydantic import BaseModel, EmailStr, Field, validator
from datetime import time
from typing import Optional, List
from enum import Enum

class CuisineType(str, Enum):
    ITALIAN = "italian"
    MEXICAN = "mexican"
    JAPANESE = "japanese"
    AMERICAN = "american"
    VEGETARIAN = "vegetarian"
    VEGAN = "vegan"
    MEDITERRANEAN = "mediterranean"
    INDIAN = "indian"
    CHINESE = "chinese"
    THAI = "thai"
    OTHER = "other"

class PriceRange(int, Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    LUXURY = 4

class RestaurantBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    address: str
    city: str
    postal_code: str
    cuisine_type: CuisineType
    opening_time: time
    closing_time: time
    capacity: int = Field(..., gt=0)
    price_range: PriceRange

    @validator('closing_time')
    def validate_times(cls, v, values):
        if 'opening_time' in values and v <= values['opening_time']:
            raise ValueError('Closing time must be after opening time')
        return v

class RestaurantCreate(RestaurantBase):
    pass

class RestaurantUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    address: Optional[str]
    city: Optional[str]
    postal_code: Optional[str]
    cuisine_type: Optional[CuisineType]
    opening_time: Optional[time]
    closing_time: Optional[time]
    capacity: Optional[int] = Field(None, gt=0)
    price_range: Optional[PriceRange]
    is_active: Optional[bool]

    @validator('closing_time')
    def validate_times(cls, v, values):
        if v is not None and 'opening_time' in values and values['opening_time'] is not None:
            if v <= values['opening_time']:
                raise ValueError('Closing time must be after opening time')
        return v

class Restaurant(RestaurantBase):
    id: int
    owner_id: int
    rating: Optional[float]
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True

class RestaurantSearchResults(BaseModel):
    results: List[Restaurant]
    total: int