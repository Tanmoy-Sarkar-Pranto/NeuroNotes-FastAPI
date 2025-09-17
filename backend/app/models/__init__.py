# app/models/__init__.py
from .user import User, UserCreate, UserRead, UserUpdate, UserLogin, UserLoginResponse
from .topic import (
    Topic,
    TopicEdge,
    TopicCreate,
    TopicRead,
    TopicReadWithEdges,
    TopicUpdate,
    TopicEdgeCreate,
    TopicEdgeRead,
    TopicEdgeUpdate,
    Position
)
from .note import Note, NoteCreate, NoteRead, NoteReadWithTags, NoteUpdate
from .tag import NoteTag, NoteTagMap, NoteTagCreate, NoteTagRead, NoteTagUpdate

__all__ = [
    # User models
    "User",
    "UserCreate",
    "UserRead",
    "UserUpdate",
    "UserLogin",
    "UserLoginResponse",

    # Topic models
    "Topic",
    "TopicEdge",
    "TopicCreate",
    "TopicRead",
    "TopicReadWithEdges",
    "TopicUpdate",
    "TopicEdgeCreate",
    "TopicEdgeRead",
    "TopicEdgeUpdate",
    "Position",

    # Note models
    "Note",
    "NoteCreate",
    "NoteRead",
    "NoteReadWithTags",
    "NoteUpdate",

    # Tag models
    "NoteTag",
    "NoteTagMap",
    "NoteTagCreate",
    "NoteTagRead",
    "NoteTagUpdate",
]