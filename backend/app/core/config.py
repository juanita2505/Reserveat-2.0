from pydantic_settings import BaseSettings
from pydantic import Field, RedisDsn, PostgresDsn, AmqpDsn
from typing import List, Optional
import secrets

class Settings(BaseSettings):
    # Configuración de la aplicación
    APP_NAME: str = "Reserveat"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    SECRET_KEY: str  # Se leerá del .env
    
    # Configuración de base de datos
    DATABASE_URL: str = "mysql+pymysql://root:123456@localhost:3306/reserveat"
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 10
    
    # Configuración de autenticación
    SECRET_KEY: str = Field(default_factory=lambda: secrets.token_urlsafe(32))
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 10080  # 7 días
    
    # Configuración de CORS (manejo especial para listas)
    CORS_ORIGINS: str = "*"
    CORS_METHODS: str = "*"
    CORS_HEADERS: str = "*"
    
    @property
    def cors_origins_list(self) -> List[str]:
        return self.CORS_ORIGINS.split(",") if self.CORS_ORIGINS else []
    
    @property
    def cors_methods_list(self) -> List[str]:
        return self.CORS_METHODS.split(",") if self.CORS_METHODS else []
    
    @property
    def cors_headers_list(self) -> List[str]:
        return self.CORS_HEADERS.split(",") if self.CORS_HEADERS else []

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()