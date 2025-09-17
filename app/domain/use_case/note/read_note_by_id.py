from app.core.domain import Error, Success
from app.data.repository import NoteRepository
from app.domain.models.note_errors import NoteError
from app.models import NoteReadWithTags


def read_note_by_id(note_id: str, user_id: str, note_repository: NoteRepository) -> Success[NoteReadWithTags] | Error[NoteError]:
    note_with_tags = note_repository.read_note_with_tags(note_id, user_id)
    if note_with_tags is None:
        return Error(NoteError.NOT_FOUND)
    return Success(note_with_tags)