import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from app.models import User, Restaurant, Reservation
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Cargar variables de entorno desde .env
load_dotenv()

# Configuración de la base de datos (usa variables de entorno con valores por defecto para Docker)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://reserveat:reserveat@db:5432/reserveat"  # Valor por defecto para Docker
)

# Crear el motor de SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    pool_size=20,  # Número máximo de conexiones
    max_overflow=10,  # Conexiones adicionales cuando se excede pool_size
    pool_pre_ping=True,  # Verifica que las conexiones estén activas
    pool_recycle=3600  # Recicla conexiones después de 1 hora
)

# Configurar la sesión de la base de datos
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False  # Útil para operaciones asíncronas
)

# Base para los modelos
Base = declarative_base()

# Función para obtener la conexión a la DB (usada en dependencias de FastAPI)
def get_db():
    """
    Generador que provee sesiones de base de datos.
    Se cierra automáticamente después de su uso.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()