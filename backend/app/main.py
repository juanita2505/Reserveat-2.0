from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import restaurants, users, reservations
from .database import engine, Base

app = FastAPI(
    title="Reserveat API",
    description="API para el sistema de reservas de restaurantes",
    version="1.0.0"
)

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