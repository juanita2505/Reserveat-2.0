import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.core.config import settings

# Cargar variables de entorno
load_dotenv()

# Configuración del motor de base de datos
engine = create_engine(
    settings.DATABASE_URL,
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW,
    pool_pre_ping=True,
    pool_recycle=3600
)

# Configuración de la sesión
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False
)

# Base declarativa (ahora se define en models/base.py)
Base = declarative_base()

def get_db():
    """Generador de sesiones de base de datos para inyección de dependencias"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()