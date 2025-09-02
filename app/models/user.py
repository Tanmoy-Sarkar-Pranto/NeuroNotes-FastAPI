# app/models/user.py
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Relationship
from pydantic import field_validator
import re

if TYPE_CHECKING:
    from .topic import Topic
    from .note import Note, NoteTag


class UserBase(SQLModel):
    username: str = Field(max_length=50, unique=True, index=True)
    email: str = Field(max_length=100, unique=True, index=True)

    @field_validator("email")
    def validate_email(cls, v: str) -> str:
        """Validate email format."""
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, v):
            raise ValueError("Invalid email format")
        return v.lower().strip()

    @field_validator("username")
    def validate_username(cls, v: str) -> str:
        """Validate username format."""
        v = v.strip()

        if len(v) < 3:
            raise ValueError("Username must be at least 3 characters long")
        if len(v) > 50:
            raise ValueError("Username must be no more than 50 characters long")

        if not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError("Username can only contain letters, numbers, underscores, and hyphens")

        if not re.match(r'^[a-zA-Z0-9]', v):
            raise ValueError("Username must start with a letter or number")

        return v.lower()


class User(UserBase, table=True):
    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    topics: List["Topic"] = Relationship(back_populates="user")
    notes: List["Note"] = Relationship(back_populates="user")
    note_tags: List["NoteTag"] = Relationship(back_populates="user")


class UserCreate(UserBase):
    password: str

    @field_validator("password")
    def validate_password(cls, v: str) -> str:
        """Validate password strength."""
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if len(v) > 128:
            raise ValueError("Password must be no more than 128 characters long")

        if not re.search(r'[A-Z]', v):
            raise ValueError("Password must contain at least one uppercase letter")

        if not re.search(r'[a-z]', v):
            raise ValueError("Password must contain at least one lowercase letter")

        if not re.search(r'\d', v):
            raise ValueError("Password must contain at least one number")

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError("Password must contain at least one special character")

        return v


class UserRead(UserBase):
    id: UUID
    created_at: datetime


class UserLogin(SQLModel):
    email: str
    password: str

class UserLoginResponse(UserRead):
    access_token: str

class UserUpdate(SQLModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None