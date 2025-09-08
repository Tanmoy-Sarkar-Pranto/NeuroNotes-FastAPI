# app/models/tag.py
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .user import User
    from .note import Note


class NoteTagBase(SQLModel):
    name: str = Field(max_length=50)
    color: Optional[str] = Field(default=None, max_length=20)


class NoteTagMap(SQLModel, table=True):
    __tablename__ = "note_tag_map"

    note_id: UUID = Field(foreign_key="notes.id", primary_key=True, ondelete="CASCADE")
    tag_id: UUID = Field(foreign_key="note_tags.id", primary_key=True, ondelete="CASCADE")

class NoteTag(NoteTagBase, table=True):
    __tablename__ = "note_tags"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", index=True, ondelete="CASCADE")
    created_at: datetime = Field(default_factory=datetime.now)

    # Relationships
    user: "User" = Relationship(back_populates="note_tags")
    notes: List["Note"] = Relationship(
        back_populates="tags",
        link_model=NoteTagMap
    )



class NoteTagCreate(NoteTagBase):
    pass


class NoteTagRead(NoteTagBase):
    id: UUID
    user_id: UUID
    created_at: datetime


class NoteTagUpdate(SQLModel):
    name: Optional[str] = None
    color: Optional[str] = None