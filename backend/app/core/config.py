from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # Configuración general
    APP_NAME: str = "Reserveat"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Configuración API
    API_V1_STR: str = "/api/v1"
    
    # Base de datos
    DATABASE_URL: str = "mysql+pymysql://root:123456@localhost:3306/reserveat"
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 10
    
    # Autenticación JWT
    SECRET_KEY: str = "tu-clave-secreta-aqui"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 10080  # 7 días
    
    # CORS (como strings separadas por comas)
    CORS_ORIGINS: str = "*"
    CORS_METHODS: str = "*"
    CORS_HEADERS: str = "*"
    
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