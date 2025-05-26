from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
import logging

from app.schemas.user import UserCreate, UserOut, UserRead  # Esquemas Pydantic para usuarios
from app.crud.user import create_user, get_user_by_email, get_user_by_username  # CRUD con función nueva
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

# Modelos Pydantic usados internamente (si quieres)
class UserRegister(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50, example="johndoe")
    password: str = Field(..., min_length=8, example="SecurePassword123")
    full_name: str = Field(..., min_length=2, example="John Doe")
    role: str = Field(default="customer")

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

@router.post("/register", response_model=UserOut, status_code=201)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        # Verificar si el usuario ya existe
        existing_email = await get_user_by_email(db, email=user.email)
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
            
        existing_username = await get_user_by_username(db, username=user.username)
        if existing_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
        
        # Crear usuario
        new_user = await create_user(db=db, user_data=user)
        await db.commit()  # Confirmar la transacción
        
        return new_user
        
    except HTTPException:
        raise  # Re-lanza las excepciones HTTP que ya manejamos
    except Exception as e:
        await db.rollback()  # Rollback en caso de error
        logger.error(f"Registration error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not register user"
        )

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    # Aquí se puede usar username o email para login, pero para estandarizar, login con username
    user = await get_user_by_username(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
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
    return current_user