# app/core/database.py
from typing import Generator, AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, create_engine, Session

from .config import settings

# Create sync engine for regular operations
engine = create_engine(
    settings.sync_database_url,
    echo=settings.DATABASE_ECHO,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=5,
    pool_recycle=300,
)

# Create async engine for async operations (if needed)
async_engine = create_async_engine(
    settings.async_database_url,
    echo=settings.DATABASE_ECHO,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=5,
    pool_recycle=300,
)

# Create session makers
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=Session,
)

AsyncSessionLocal = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


def create_db_and_tables():
    """Create database tables. Use this in main.py startup event."""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """
    Dependency to get database session.
    Use this as a FastAPI dependency.

    Example usage:
    @app.get("/users/")
    def get_users(session: Session = Depends(get_session)):
        ...
    """
    with SessionLocal() as session:
        try:
            yield session
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Async dependency to get database session.
    Use this for async endpoints.

    Example usage:
    @app.get("/users/")
    async def get_users(session: AsyncSession = Depends(get_async_session)):
        ...
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
