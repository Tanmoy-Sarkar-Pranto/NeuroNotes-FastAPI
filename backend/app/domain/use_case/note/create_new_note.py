from datetime import datetime

from app.core.domain import Error, Success
from app.data.repository import NoteRepository
from app.domain.models.note_errors import NoteError
from app.models import NoteReadWithTags, NoteCreate, Note


def create_new_note(note: NoteCreate, user_id: str, note_repository: NoteRepository) -> Success[NoteReadWithTags] | Error[NoteError]:
    # Extract tag_ids before creating note (since Note model doesn't have tag_ids field)
    note_data = note.model_dump()
    tag_ids = note_data.pop('tag_ids', None)
    
    # Validate tags belong to user if provided
    if tag_ids and not note_repository.validate_tags_belong_to_user(tag_ids, user_id):
        return Error(NoteError.INVALID_TAGS)
    
    # Create note
    db_note = Note(
        **note_data,
        user_id=user_id,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    created_note = note_repository.create_note(db_note)
    
    # Associate tags if provided
    if tag_ids:
        note_repository.set_note_tags(created_note.id, tag_ids)
    
    # Get the created note with tags
    note_with_tags = note_repository.read_note_with_tags(str(created_note.id), user_id)
    return Success(note_with_tags)