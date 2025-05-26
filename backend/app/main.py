from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.database import engine, Base 
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.database import engine, Base  # Asegúrate que engine sea AsyncEngine
from app.api.v1.endpoints import auth, users, restaurants, reservations


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=settings.cors_methods_list,
    allow_headers=settings.cors_headers_list,
)

# Routers
app.include_router(
    auth.router,
    prefix=settings.API_V1_STR,
    tags=["auth"]
)
app.include_router(
    users.router,
    prefix=settings.API_V1_STR,
    tags=["users"]
)
app.include_router(
    restaurants.router,
    prefix=settings.API_V1_STR,
    tags=["restaurants"]
)
app.include_router(
    reservations.router,
    prefix=settings.API_V1_STR,
    tags=["reservations"]
)

# Startup event for creating tables (async)
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to Reserveat API",
        "version": settings.APP_VERSION
    }

from app.api.v1.endpoints import auth, users, restaurants, reservations

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=settings.cors_methods_list,
    allow_headers=settings.cors_headers_list,
)

# Routers
app.include_router(
    auth.router,
    prefix=settings.API_V1_STR,
    tags=["auth"]
)
app.include_router(
    users.router,
    prefix=settings.API_V1_STR,
    tags=["users"]
)
app.include_router(
    restaurants.router,
    prefix=settings.API_V1_STR,
    tags=["restaurants"]
)
app.include_router(
    reservations.router,
    prefix=settings.API_V1_STR,
    tags=["reservations"]
)

# Startup event for creating tables (async)
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to Reserveat API",
        "version": settings.APP_VERSION
    }
