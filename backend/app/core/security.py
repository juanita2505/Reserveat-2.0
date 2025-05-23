from datetime import datetime, timedelta
from typing import Any, Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.user import User
from app.database import get_db
from app.schemas.user import UserRole
import logging

# Configuración de logging
logger = logging.getLogger(__name__)

# Configuración de seguridad
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="api/v1/auth/login",
    scheme_name="JWT"
)
security = HTTPBearer()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica si la contraseña coincide con el hash"""
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        logger.error(f"Error verifying password: {e}")
        return False

def get_password_hash(password: str) -> str:
    """Genera un hash seguro de la contraseña"""
    return pwd_context.hash(password)

def create_access_token(
    subject: Any,
    expires_delta: Optional[timedelta] = None,
    refresh: bool = False,
    additional_claims: Optional[dict] = None
) -> str:
    """
    Crea un token JWT con claims adicionales opcionales
    Args:
        subject: Identificador del usuario (normalmente user.id)
        expires_delta: Tiempo de expiración personalizado
        refresh: Si es un refresh token
        additional_claims: Claims adicionales para incluir en el token
    """
    expire_minutes = settings.REFRESH_TOKEN_EXPIRE_MINUTES if refresh else settings.ACCESS_TOKEN_EXPIRE_MINUTES
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=expire_minutes))
    
    to_encode = {
        "sub": str(subject),
        "exp": expire,
        "type": "refresh" if refresh else "access",
        "iat": datetime.utcnow(),
    }
    
    if additional_claims:
        to_encode.update(additional_claims)
    
    try:
        return jwt.encode(
            to_encode,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )
    except Exception as e:
        logger.error(f"Error creating token: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not create token"
        )

async def get_token_from_request(request: Request) -> str:
    """Extrae el token del header Authorization"""
    credentials: HTTPAuthorizationCredentials = await security(request)
    if not credentials or not credentials.scheme == "Bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication scheme"
        )
    return credentials.credentials

async def get_current_user(
    request: Request,
    db: Session = Depends(get_db),
    token: str = Depends(get_token_from_request)
) -> User:
    """Obtiene el usuario actual a partir del token JWT"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        token_type: str = payload.get("type")
        
        if not user_id or token_type != "access":
            logger.warning(f"Invalid token claims: {payload}")
            raise credentials_exception
            
        user = db.query(User).filter(User.id == int(user_id)).first()
        if not user:
            logger.warning(f"User not found: {user_id}")
            raise credentials_exception
            
        # Verificar si el token ha sido revocado (opcional)
        # if user.token_version != payload.get("ver"):
        #     raise credentials_exception
            
    except JWTError as e:
        logger.error(f"JWT Error: {e}")
        raise credentials_exception
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
    
    # Almacenar el usuario en el request para uso posterior
    request.state.user = user
    return user

async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Verifica que el usuario esté activo"""
    if not current_user.is_active:
        logger.warning(f"Inactive user attempt: {current_user.id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    return current_user

def role_required(*required_roles: UserRole):
    """Decorador para verificar múltiples roles de usuario"""
    def role_checker(current_user: User = Depends(get_current_active_user)):
        if current_user.role not in required_roles:
            logger.warning(
                f"Role violation: User {current_user.id} "
                f"with role {current_user.role} "
                f"tried to access {required_roles}"
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation not permitted for your role"
            )
        return current_user
    return role_checker

def create_tokens(user_id: int, additional_claims: Optional[dict] = None) -> dict:
    """Crea ambos tokens (access y refresh) con claims adicionales opcionales"""
    return {
        "access_token": create_access_token(user_id, additional_claims=additional_claims),
        "refresh_token": create_access_token(user_id, refresh=True, additional_claims=additional_claims),
        "token_type": "bearer"
    }

def verify_refresh_token(token: str) -> dict:
    """Verifica un refresh token y devuelve el payload si es válido"""
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        if payload.get("type") != "refresh":
            raise JWTError("Invalid token type")
        return payload
    except JWTError as e:
        logger.error(f"Invalid refresh token: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )