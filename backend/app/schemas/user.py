from pydantic import BaseModel, EmailStr, ConfigDict, Field
from typing import Optional
from enum import Enum

class UserRole(str, Enum):
    customer = "customer"
    restaurant_owner = "restaurant_owner"
    admin = "admin"

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, example="john_doe")  
    email: EmailStr
    full_name: str = Field(..., min_length=2, max_length=100)
    role: str = Field(default="customer")

class UserCreate(UserBase):
    full_name: str
    email: EmailStr
    password: str
    role: str
    username: str

class User(UserBase):
    id: int
    is_active: bool
    model_config = ConfigDict(from_attributes=True)

class UserOut(User):
    pass

class UserRead(UserOut):
    pass

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None