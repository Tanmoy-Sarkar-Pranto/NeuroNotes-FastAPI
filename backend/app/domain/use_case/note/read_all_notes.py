from typing import List

from app.core.domain import Error, Success
from app.data.repository import NoteRepository
from app.domain.models.note_errors import NoteError
from app.models import NoteReadWithTags


def read_all_notes_by_topic_id(topic_id: str, user_id: str, note_repository: NoteRepository) -> Success[List[NoteReadWithTags]] | Error[NoteError]:
    notes_with_tags = note_repository.read_all_notes_with_tags(topic_id, user_id)
    if not notes_with_tags:
        return Error(NoteError.NOT_FOUND)
    return Success(notes_with_tags)