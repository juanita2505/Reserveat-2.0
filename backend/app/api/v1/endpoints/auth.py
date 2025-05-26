from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
import logging

from app.schemas.user import UserRead
from app.crud.user import create_user, get_user_by_email
from app.core.security import (
    verify_password,
    create_access_token,
    get_current_user
)
from app.database import get_db
from app.core.config import settings

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

logger = logging.getLogger(__name__)

# Modelos Pydantic
class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, example="SecurePassword123")
    full_name: str = Field(..., min_length=2, example="John Doe")
    role: str = Field(default="customer")

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserRegister,
    db: AsyncSession = Depends(get_db)
):
    """
    Register a new user account.
    Required fields:
    - email: valid email address
    - password: at least 8 characters
    - full_name: at least 2 characters
    Optional field:
    - role: defaults to 'customer'
    """
    try:
        db_user = await get_user_by_email(db, email=user_data.email)
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        user = await create_user(db=db, user=user_data)
        return user
    except Exception as e:
        logger.error(f"Registration error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed. Please try again."
        )

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """
    Authenticate user and return access token.
    Uses standard OAuth2 password flow.
    Required form data:
    - username: user's email
    - password: user's password
    """
    user = await get_user_by_email(db, email=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get("/me", response_model=UserRead)
async def read_user_me(
    current_user: UserRead = Depends(get_current_user)
):
    """
    Get current authenticated user's information
    """
    return current_user