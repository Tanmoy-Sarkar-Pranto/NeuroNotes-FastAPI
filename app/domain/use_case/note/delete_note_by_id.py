from app.core.domain import Error, Success
from app.data.repository import NoteRepository
from app.domain.models.note_errors import NoteError


def delete_note_by_id(note_id: str, user_id: str, note_repository: NoteRepository) -> Success[bool] | Error[NoteError]:
    note = note_repository.delete_note(note_id, user_id)
    if not note:
        return Error(NoteError.NOT_FOUND)
    return Success(True)