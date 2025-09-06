# app/api/deps.py
from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt  # <-- using PyJWT
from jwt import PyJWTError  # Base class for all errors
from sqlmodel import Session
from uuid import UUID

from app.core.database import get_session
from app.core.config import settings
from app.data.repository import UserRepository
from app.models.user import User

# Security scheme
security = HTTPBearer()


def get_db() -> Generator[Session, None, None]:
    """Database session dependency - alias for get_session for convenience."""
    yield from get_session()


def get_current_user_id(
        credentials: HTTPAuthorizationCredentials = Depends(security),
) -> UUID:
    """
    Extract user ID from JWT token.
    Use this when you only need the user ID (more efficient).
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        user_id: str | None = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        return UUID(user_id)
    except (PyJWTError, ValueError):
        raise credentials_exception


def get_current_user(
        session: Session = Depends(get_db),
        user_id: UUID = Depends(get_current_user_id),
) -> User:
    """
    Get current authenticated user object.
    Use this when you need the full user object.
    """
    user = session.get(User, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


def get_current_active_user(
        current_user: User = Depends(get_current_user),
) -> User:
    """
    Get current active user (extend this if you add user status fields).
    """
    # Add any additional checks here (e.g., user.is_active, user.is_verified)
    return current_user


def get_user_repository(session: Session = Depends(get_db)):
    return UserRepository(session)