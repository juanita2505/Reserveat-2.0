from datetime import datetime, timedelta
from typing import Any, Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.user import User
from app.database import get_db
from app.schemas.user import UserRole
import logging

# Configuración
logger = logging.getLogger(__name__)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login",
    scheme_name="JWT"
)

# Funciones de contraseña
def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        logger.error(f"Error verifying password: {e}")
        return False

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Funciones JWT
def create_access_token(
    subject: Any,
    expires_delta: Optional[timedelta] = None,
    refresh: bool = False
) -> str:
    expire_minutes = settings.REFRESH_TOKEN_EXPIRE_MINUTES if refresh else settings.ACCESS_TOKEN_EXPIRE_MINUTES
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=expire_minutes))
    
    to_encode = {
        "sub": str(subject),
        "exp": expire,
        "type": "refresh" if refresh else "access"
    }
    
    try:
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    except Exception as e:
        logger.error(f"Error creating token: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not create token"
        )

# Autenticación
async def get_current_user(
    request: Request,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if not user_id:
            raise credentials_exception
            
        user = db.query(User).filter(User.id == int(user_id)).first()
        if not user:
            raise credentials_exception
            
        request.state.user = user
        return user
    except JWTError as e:
        logger.error(f"JWT Error: {e}")
        raise credentials_exception

async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    return current_user

# Control de roles
def has_role(required_role: UserRole):
    def role_checker(current_user: User = Depends(get_current_active_user)):
        if current_user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation not permitted"
            )
        return current_user
    return role_checker