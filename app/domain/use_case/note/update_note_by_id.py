from datetime import datetime

from app.core.domain import Error, Success
from app.data.repository import NoteRepository
from app.domain.models.note_errors import NoteError
from app.models import NoteRead, NoteUpdate


def update_note_by_id(note_id: str, user_id: str, note: NoteUpdate, note_repository: NoteRepository) -> Success[NoteRead] | Error[NoteError]:
    existing_note = note_repository.read_note_by_id(note_id, user_id)
    if existing_note is None:
        return Error(NoteError.NOT_FOUND)

    existing_note.title = note.title or existing_note.title
    existing_note.content = note.content or existing_note.content
    existing_note.updated_at = datetime.now()
    existing_note.urls = note.urls or existing_note.urls

    note = note_repository.update_note(existing_note)
    note_read = NoteRead(**note.model_dump())
    return Success(note_read)