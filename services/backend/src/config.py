import os

from logging import config as logging_config
from src.logger import LOGGING
from pydantic import Field
from pydantic_settings import BaseSettings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

logging_config.dictConfig(LOGGING)

class Settings(BaseSettings):
    project_name: str = Field(..., alias="BACKEND_PROJECT_NAME")
    service_host: str = Field(..., alias="BACKEND_HOST")
    service_port: int = Field(..., alias="BACKEND_PORT")
    is_debug: bool = Field(..., alias="BACKEND_DEBUG")
    blocked_ips: list[str] = []
    
    @property    
    def service_url(self) -> str:
        return f"http://{'127.0.0.1' if self.is_debug else self.service_host}:{self.service_port}"
    
settings = Settings()

class PostgresSettings(BaseSettings):
    db: str = Field(..., alias='DB_NAME')
    user: str = Field(..., alias='DB_USER')
    password: str = Field(..., alias='DB_PASSWORD')
    host: str = Field(..., alias='DB_HOST')
    port: int = Field(..., alias='DB_PORT')
    
    @property
    def async_dsn(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"

    @property
    def sync_dsn(self) -> str:
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"


pg = PostgresSettings()