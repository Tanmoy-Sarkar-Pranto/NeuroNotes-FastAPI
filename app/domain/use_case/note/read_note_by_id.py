from app.core.domain import Error, Success
from app.data.repository import NoteRepository
from app.domain.models.note_errors import NoteError
from app.models import NoteRead


def read_note_by_id(topic_id: str, user_id: str, note_repository: NoteRepository) -> Success[NoteRead] | Error[NoteError]:
    note = note_repository.read_note_by_id(topic_id, user_id)
    if note is None:
        return Error(NoteError.NOT_FOUND)
    note_read = NoteRead(**note.model_dump())
    return Success(note_read)