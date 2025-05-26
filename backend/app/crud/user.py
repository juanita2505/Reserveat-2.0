from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash
from typing import Optional, List, Union
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)

# Modelo Pydantic para registro de usuarios (si no está en otro archivo)
class UserRegister(BaseModel):
    email: str
    password: str
    full_name: str
    role: str = "customer"

async def get_user(db: AsyncSession, user_id: int) -> Optional[User]:
    """Obtiene un usuario por ID"""
    try:
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()
    except Exception as e:
        logger.error(f"Error getting user by ID {user_id}: {str(e)}")
        raise

async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    """Obtiene un usuario por email"""
    try:
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()
    except Exception as e:
        logger.error(f"Error getting user by email {email}: {str(e)}")
        raise

async def get_users(
    db: AsyncSession, 
    skip: int = 0, 
    limit: int = 100,
    search: Optional[str] = None
) -> List[User]:
    """Lista usuarios con paginación y búsqueda"""
    try:
        query = select(User)
        
        if search:
            query = query.where(
                or_(
                    User.email.ilike(f"%{search}%"),
                    User.full_name.ilike(f"%{search}%")
                )
            )
            
        result = await db.execute(query.offset(skip).limit(limit))
        return result.scalars().all()
    except Exception as e:
        logger.error(f"Error listing users: {str(e)}")
        raise

async def create_user(
    db: AsyncSession, 
    user_data: Union[UserCreate, UserRegister]
) -> User:
    """Crea un nuevo usuario con manejo seguro de roles"""
    try:
        hashed_password = get_password_hash(user_data.password)
        
        # Validación del rol
        try:
            role = UserRole(user_data.role.lower())
        except ValueError:
            role = UserRole.CUSTOMER
            logger.warning(f"Invalid role '{user_data.role}', defaulting to CUSTOMER")

        db_user = User(
            email=user_data.email,
            hashed_password=hashed_password,
            full_name=user_data.full_name,
            role=role,
            is_active=True
        )
        
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user
        
    except Exception as e:
        await db.rollback()
        logger.error(f"Error creating user: {str(e)}")
        raise

async def update_user(
    db: AsyncSession, 
    user_id: int, 
    user_data: UserUpdate
) -> Optional[User]:
    """Actualiza un usuario existente con manejo seguro de contraseñas"""
    try:
        db_user = await get_user(db, user_id)
        if not db_user:
            return None

        update_data = user_data.dict(exclude_unset=True)
        
        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
        
        for key, value in update_data.items():
            setattr(db_user, key, value)
            
        await db.commit()
        await db.refresh(db_user)
        return db_user
        
    except Exception as e:
        await db.rollback()
        logger.error(f"Error updating user {user_id}: {str(e)}")
        raise

async def delete_user(db: AsyncSession, user_id: int) -> bool:
    """Elimina un usuario de forma segura"""
    try:
        db_user = await get_user(db, user_id)
        if not db_user:
            return False

        await db.delete(db_user)
        await db.commit()
        return True
        
    except Exception as e:
        await db.rollback()
        logger.error(f"Error deleting user {user_id}: {str(e)}")
        raise