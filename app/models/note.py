# app/models/note.py
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Relationship, Column
from sqlalchemy import ARRAY, String

from .tag import NoteTagMap
if TYPE_CHECKING:
    from .user import User
    from .topic import Topic
    from .tag import NoteTag, NoteTagRead


class NoteBase(SQLModel):
    title: Optional[str] = Field(default=None, max_length=255)
    content: str
    urls: Optional[List[str]] = Field(default=None, sa_column=Column(ARRAY(String)))


class Note(NoteBase, table=True):
    __tablename__ = "notes"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    topic_id: UUID = Field(foreign_key="topics.id", index=True, ondelete="CASCADE")
    user_id: UUID = Field(foreign_key="users.id", index=True, ondelete="CASCADE")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    # Relationships
    topic: "Topic" = Relationship(back_populates="notes")
    user: "User" = Relationship(back_populates="notes")
    tags: List["NoteTag"] = Relationship(
        back_populates="notes",
        link_model=NoteTagMap
    )


class NoteCreate(NoteBase):
    topic_id: UUID
    tag_ids: Optional[List[UUID]] = None  # For assigning tags during creation


class NoteRead(NoteBase):
    id: UUID
    topic_id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime


class NoteReadWithTags(NoteRead):
    tags: List["NoteTagRead"] = []


class NoteUpdate(SQLModel):
    title: Optional[str] = None
    content: Optional[str] = None
    urls: Optional[List[str]] = None
    tag_ids: Optional[List[UUID]] = None  # For updating tags