from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash
from typing import Optional, List

async def get_user(db: AsyncSession, user_id: int) -> Optional[User]:
    """Obtiene un usuario por ID (asíncrono)"""
    result = await db.execute(select(User).filter(User.id == user_id))
    return result.scalar_one_or_none()

async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    """Obtiene un usuario por email (asíncrono)"""
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalar_one_or_none()

async def get_users(
    db: AsyncSession, 
    skip: int = 0, 
    limit: int = 100,
    search: Optional[str] = None
) -> List[User]:
    """Lista usuarios con paginación y búsqueda (asíncrono)"""
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

async def create_user(db: AsyncSession, user: UserCreate) -> User:
    """Crea un nuevo usuario (asíncrono)"""
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name,
        role=user.role,
        is_active=True
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def update_user(
    db: AsyncSession, 
    user_id: int, 
    user: UserUpdate
) -> Optional[User]:
    """Actualiza un usuario existente (asíncrono)"""
    db_user = await get_user(db, user_id)
    if db_user:
        update_data = user.dict(exclude_unset=True)
        
        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
        
        for key, value in update_data.items():
            setattr(db_user, key, value)
        
        await db.commit()
        await db.refresh(db_user)
    return db_user

async def delete_user(db: AsyncSession, user_id: int) -> bool:
    """Elimina un usuario (asíncrono)"""
    db_user = await get_user(db, user_id)
    if db_user:
        await db.delete(db_user)
        await db.commit()
        return True
    return False