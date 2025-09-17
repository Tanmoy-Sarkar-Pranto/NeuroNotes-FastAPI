# app/core/config.py
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str = "postgresql://postgres:1234@localhost:5432/neuronotes"
    ASYNC_DATABASE_URL: str = "postgresql+asyncpg://postgres:1234@localhost:5432/neuronotes"
    DATABASE_ECHO: bool = False

    # Security settings
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Topics Knowledge Graph"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "A knowledge management system with graph visualization"

    # CORS settings
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:5173"]

    # Environment
    ENVIRONMENT: str = "development"

    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100

    # Vector embeddings (if using OpenAI or similar)
    OPENAI_API_KEY: Optional[str] = None
    EMBEDDING_MODEL: str = "text-embedding-ada-002"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()