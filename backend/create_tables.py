import asyncio
import sys
from pathlib import Path

# Añade el directorio backend al path
sys.path.append(str(Path(__file__).parent))

from app.database import engine, Base
from app.models.user import User
from app.models.restaurant import Restaurant
from app.models.reservation import Reservation

async def create_tables():
    print("⚙️ Creando tablas en la base de datos...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Tablas creadas exitosamente!")
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(create_tables())
