from datetime import datetime

from app.core.domain import Error, Success
from app.data.repository import NoteRepository
from app.domain.models.note_errors import NoteError
from app.models import NoteReadWithTags, NoteUpdate


def update_note_by_id(note_id: str, user_id: str, note_update: NoteUpdate, note_repository: NoteRepository) -> Success[NoteReadWithTags] | Error[NoteError]:
    existing_note = note_repository.read_note_by_id(note_id, user_id)
    if existing_note is None:
        return Error(NoteError.NOT_FOUND)

    # Extract tag_ids from update data
    update_data = note_update.model_dump(exclude_unset=True)
    tag_ids = update_data.pop('tag_ids', None)
    
    # Validate tags belong to user if provided
    if tag_ids is not None and not note_repository.validate_tags_belong_to_user(tag_ids, user_id):
        return Error(NoteError.INVALID_TAGS)

    # Update note fields
    existing_note.title = note_update.title if note_update.title is not None else existing_note.title
    existing_note.content = note_update.content if note_update.content is not None else existing_note.content
    existing_note.updated_at = datetime.now()
    existing_note.urls = note_update.urls if note_update.urls is not None else existing_note.urls

    updated_note = note_repository.update_note(existing_note)
    
    # Update tag associations if tag_ids provided (including empty list to clear all tags)
    if tag_ids is not None:
        note_repository.set_note_tags(updated_note.id, tag_ids)
    
    # Get the updated note with tags
    note_with_tags = note_repository.read_note_with_tags(note_id, user_id)
    return Success(note_with_tags)