import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import declarative_base
from app.core.config import settings

# Cargar variables de entorno
load_dotenv()

# Configuración del motor ASINCRONO para MySQL
engine = create_async_engine(
    settings.DATABASE_URL,  # Usa la URL directamente sin reemplazar
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=True
)

# Configuración de la sesión ASINCRONA
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base declarativa
Base = declarative_base(cls=AsyncAttrs)

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()