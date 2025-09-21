# app/core/config.py
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str
    ASYNC_DATABASE_URL: Optional[str] = None
    DATABASE_ECHO: bool = False

    @property
    def async_database_url(self) -> str:
        """Return an async-compatible DB URL.

        - Prefer explicit ASYNC_DATABASE_URL if provided
        - Otherwise convert postgres[ql] scheme to asyncpg driver
        """
        if self.ASYNC_DATABASE_URL:
            return self.ASYNC_DATABASE_URL

        url = self.DATABASE_URL
        # Normalize any postgres scheme variants to asyncpg
        if url.startswith("postgresql://"):
            return url.replace("postgresql://", "postgresql+asyncpg://", 1)
        if url.startswith("postgres://"):
            return url.replace("postgres://", "postgresql+asyncpg://", 1)
        return url

    @property
    def sync_database_url(self) -> str:
        """Return a sync-compatible DB URL for SQLAlchemy/psycopg.

        Normalizes 'postgres://' to 'postgresql://' as needed.
        """
        url = self.DATABASE_URL
        if url.startswith("postgres://"):
            return url.replace("postgres://", "postgresql://", 1)
        return url

    # Security settings
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "NeuroNotes"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "A knowledge management system with graph visualization"

    # CORS settings
    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:5174"
    ]

    # Add method to parse CORS origins from environment
    def get_cors_origins(self) -> list[str]:
        if self.ENVIRONMENT == "production":
            # In production, CORS should be set via environment variable
            import os
            cors_origins = os.getenv("BACKEND_CORS_ORIGINS")
            if cors_origins:
                # Parse JSON string from environment
                import json
                try:
                    return json.loads(cors_origins)
                except json.JSONDecodeError:
                    return cors_origins.split(",")
        return self.BACKEND_CORS_ORIGINS

    # Environment
    ENVIRONMENT: str = "development"

    # Production settings
    PORT: int = 8000

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
