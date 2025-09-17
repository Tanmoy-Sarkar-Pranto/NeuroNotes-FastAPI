from typing import List

from app.core.domain import Error, Success
from app.data.repository import NoteRepository
from app.domain.models.note_errors import NoteError
from app.models import NoteRead


def read_all_notes_by_topic_id(topic_id: str, user_id: str, note_repository: NoteRepository) -> Success[List[NoteRead]] | Error[NoteError]:
    notes = note_repository.read_all_notes(topic_id, user_id)
    if notes is None:
        return Error(NoteError.NOT_FOUND)
    note_read_list = []
    for note in notes:
        note_read_list.append(NoteRead(
            id=note.id,
            topic_id=note.topic_id,
            title=note.title,
            content=note.content,
            urls=note.urls,
            created_at=note.created_at,
            updated_at=note.updated_at,
        ))
    return Success(note_read_list)