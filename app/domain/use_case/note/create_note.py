from datetime import datetime

from app.core.domain import Error, Success
from app.data.repository import NoteRepository
from app.domain.models.note_errors import NoteError
from app.models import NoteRead, NoteCreate, Note


def create_note(note: NoteCreate, user_id: str, note_repository: NoteRepository) -> Success[NoteRead] | Error[NoteError]:
    note = Note(
        **note.model_dump(),
        user_id=user_id,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    note = note_repository.create_note(note)
    note_read = NoteRead(**note.model_dump())
    return Success(note_read)