import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# Cargar variables de entorno
load_dotenv()

# Configuración del motor ASINCRONO (nota el create_async_engine)
engine = create_async_engine(
    settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"),  # Asegúrate de usar el driver async
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=True  # Opcional: muestra las queries en consola
)

# Configuración de la sesión ASINCRONA
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False
)

# Base declarativa para modelos asíncronos
Base = declarative_base(cls=AsyncAttrs)

# Función para inyección de dependencias
async def get_db():
    """Generador de sesiones asíncronas para inyección de dependencias"""
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()