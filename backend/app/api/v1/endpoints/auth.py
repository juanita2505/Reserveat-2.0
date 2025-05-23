from fastapi import APIRouter, HTTPException, status, Depends
from typing import Optional

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

# Ejemplo básico de endpoints
@router.post("/login")
async def login():
    return {"message": "Login endpoint"}

@router.post("/register")
async def register():
    return {"message": "Register endpoint"}