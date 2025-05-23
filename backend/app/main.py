from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import restaurants, users, reservations
from app.models.user import User
from app.models.restaurant import Restaurant
from .database import engine, Base
import sys
from pathlib import Path

# Añade esto al inicio del archivo
sys.path.append(str(Path(__file__).parent.parent.parent))

from fastapi import FastAPI
from app.api.v1.endpoints import restaurants, users, reservations

app = FastAPI()

app.include_router(restaurants.router, prefix="/api/v1/restaurants", tags=["restaurants"])

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crear tablas de la base de datos
Base.metadata.create_all(bind=engine)

# Incluir routers
app.include_router(restaurants.router)
app.include_router(users.router)
app.include_router(reservations.router)

@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Bienvenido a Reserveat API",
        "docs": "/docs",
        "redoc": "/redoc"
    }