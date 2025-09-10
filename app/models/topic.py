# app/models/topic.py
from datetime import datetime
from typing import Optional, List, Dict, Any, TYPE_CHECKING
from uuid import UUID, uuid4

from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship, Column, JSON, UniqueConstraint

if TYPE_CHECKING:
    from .user import User
    from .note import Note

class Position(BaseModel):
    x: float
    y: float

class TopicBase(SQLModel):
    title: str = Field(max_length=255)
    description: Optional[str] = None
    node_type: Optional[str] = Field(default=None, max_length=20)
    position: Optional[Position] = Field(default=None, sa_column=Column(JSON))


class Topic(TopicBase, table=True):
    __tablename__ = "topics"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", index=True, ondelete="CASCADE")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    __table_args__ = (UniqueConstraint("title", "user_id", name="uq_user_topic_title"),)

    # Relationships
    user: "User" = Relationship(back_populates="topics")
    notes: List["Note"] = Relationship(back_populates="topic")

    # Edge relationships
    outgoing_edges: List["TopicEdge"] = Relationship(
        back_populates="source_topic",
        sa_relationship_kwargs={"foreign_keys": "TopicEdge.source"}
    )
    incoming_edges: List["TopicEdge"] = Relationship(
        back_populates="target_topic",
        sa_relationship_kwargs={"foreign_keys": "TopicEdge.target"}
    )


class TopicEdgeBase(SQLModel):
    relation_type: Optional[str] = Field(default=None, max_length=50)
    edge_metadata: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON))


class TopicEdge(TopicEdgeBase, table=True):
    __tablename__ = "topic_edges"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    source: UUID = Field(foreign_key="topics.id", index=True, ondelete="CASCADE")
    target: UUID = Field(foreign_key="topics.id", index=True, ondelete="CASCADE")

    # Relationships
    source_topic: Topic = Relationship(
        back_populates="outgoing_edges",
        sa_relationship_kwargs={"foreign_keys": "TopicEdge.source"}
    )
    target_topic: Topic = Relationship(
        back_populates="incoming_edges",
        sa_relationship_kwargs={"foreign_keys": "TopicEdge.target"}
    )


# Pydantic schemas for API
class TopicCreate(TopicBase):
    related_topics: Optional[List[UUID]] = None  # For creating edges
    relation_types: Optional[List[str]] = None   # Corresponding relation types


class TopicRead(TopicBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime


class TopicReadWithEdges(TopicRead):
    outgoing_edges: List["TopicEdgeRead"] = []
    incoming_edges: List["TopicEdgeRead"] = []


class TopicUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    node_type: Optional[str] = None
    position: Optional[Position] = Field(default=None, sa_column=Column(JSON))


class TopicEdgeCreate(TopicEdgeBase):
    source: UUID
    target: UUID


class TopicEdgeRead(TopicEdgeBase):
    id: UUID
    source: UUID
    target: UUID


class TopicEdgeUpdate(SQLModel):
    relation_type: Optional[str] = None
    edge_metadata: Optional[Dict[str, Any]] = None