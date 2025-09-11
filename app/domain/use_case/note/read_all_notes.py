from typing import List

from app.core.domain import Error, Success
from app.data.repository import NoteRepository
from app.domain.models.note_errors import NoteError
from app.models import NoteRead


def read_all_notes(user_id: str, note_repository: NoteRepository) -> Success[List[NoteRead]] | Error[NoteError]:
    notes = note_repository.read_all_notes(user_id)
    if notes is None:
        return Error(NoteError.NOT_FOUND)
    note_read_list = []
    for note in notes:
        note_read_list.append(NoteRead(**note.model_dump()))
    return Success(note_read_list)