from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Configuración general de la aplicación
    APP_NAME: str = "Reserveat"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Configuración de la API
    API_V1_STR: str = "/api/v1"  # Prefijo para endpoints de la API
    
    # Configuración de base de datos
    DATABASE_URL: str = "mysql+pymysql://root:123456@localhost:3306/reserveat"
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 10
    
    # Configuración de autenticación JWT
    SECRET_KEY: str = "tu-clave-secreta-muy-segura-aqui-cambiar-por-una-real"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # 30 minutos
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 10080  # 7 días (en minutos)
    
    # Configuración de CORS (opcional)
    CORS_ORIGINS: list = ["*"]
    CORS_METHODS: list = ["*"]
    CORS_HEADERS: list = ["*"]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True  # Opcional: para ser estricto con mayúsculas/minúsculas

settings = Settings()