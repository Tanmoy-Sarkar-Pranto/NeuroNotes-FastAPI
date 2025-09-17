from datetime import datetime

from app.core.domain import Error, Success
from app.data.repository import NoteRepository
from app.domain.models.note_errors import NoteError
from app.models import NoteRead, NoteCreate, Note


def create_new_note(note: NoteCreate, user_id: str, note_repository: NoteRepository) -> Success[NoteRead] | Error[NoteError]:
    note = Note(
        **note.model_dump(),
        user_id=user_id,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    created_note = note_repository.create_note(note)
    note_read = NoteRead(
        id=created_note.id,
        topic_id=created_note.topic_id,
        title=created_note.title,
        content=created_note.content,
        urls=created_note.urls,
        created_at=created_note.created_at,
        updated_at=created_note.updated_at,
    )
    return Success(note_read)