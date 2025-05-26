import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.models.base import Base
from app.models.user import User
from app.models.restaurant import Restaurant
from app.models.reservation import Reservation
from app.core.config import settings

async def create_tables():
    print("⚙️ Creando tablas en la base de datos...")
    
    # Configuración de la conexión
    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=True  # Muestra las consultas SQL en consola
    )
    
    async with engine.begin() as conn:
        # Elimina todas las tablas existentes (opcional, cuidado en producción)
        # await conn.run_sync(Base.metadata.drop_all)
        
        # Crea todas las tablas
        await conn.run_sync(Base.metadata.create_all)
    
    print("✅ Tablas creadas exitosamente!")
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(create_tables())