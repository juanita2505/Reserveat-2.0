from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User

def get_current_user_role(required_role: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    """Dependencia para verificar roles de usuario"""
    if current_user.role != required_role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para realizar esta acción"
        )
    return current_user

def get_db_session(db: Session = Depends(get_db)):
    """Proveedor de sesión de base de datos simplificado"""
    return db