from pydantic_settings import BaseSettings
from pydantic import Field, PostgresDsn
from typing import List, ClassVar, Optional

class Settings(BaseSettings):
    # Configuración general
    APP_NAME: str = "Reserveat"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Configuración API
    API_V1_STR: str = "/api/v1"
    
    # Base de datos (corregido con anotación de tipo)
    DATABASE_URL: str = Field(
        default="mysql+aiomysql://root:123456@localhost:3306/reserveat",
        description="URL de conexión a la base de datos"
    )
    
    DATABASE_POOL_SIZE: int = Field(
        default=20,
        ge=1,
        description="Tamaño del pool de conexiones"
    )
    
    DATABASE_MAX_OVERFLOW: int = Field(
        default=10,
        ge=0,
        description="Conexiones adicionales máximas"
    )
    
    # Autenticación JWT
    SECRET_KEY: str = Field(
        default="tu-clave-secreta-aqui",
        min_length=32,
        description="Clave para firmar tokens JWT"
    )
    
    ALGORITHM: str = Field(
        default="HS256",
        description="Algoritmo de firma JWT"
    )
    
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=30,
        gt=0,
        description="Expiración token acceso (min)"
    )
    
    REFRESH_TOKEN_EXPIRE_MINUTES: int = Field(
        default=10080,
        description="Expiración token refresco (min)"
    )
    
    # CORS
    CORS_ORIGINS: str = Field(
        default="*",
        description="Orígenes permitidos separados por comas"
    )
    
    CORS_METHODS: str = Field(
        default="*",
        description="Métodos HTTP permitidos"
    )
    
    CORS_HEADERS: str = Field(
        default="*",
        description="Cabeceras permitidas"
    )

    # Propiedades calculadas
    @property
    def cors_origins_list(self) -> List[str]:
        return self._split_cors_value(self.CORS_ORIGINS)
    
    @property
    def cors_methods_list(self) -> List[str]:
        return self._split_cors_value(self.CORS_METHODS)
    
    @property
    def cors_headers_list(self) -> List[str]:
        return self._split_cors_value(self.CORS_HEADERS)
    
    def _split_cors_value(self, value: str) -> List[str]:
        if not value:
            return []
        if value.strip() == "*":
            return ["*"]
        return [item.strip() for item in value.split(",")]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()