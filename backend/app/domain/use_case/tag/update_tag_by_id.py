from app.core.domain import Success, Error
from app.data.repository.tag import TagRepository
from app.domain.models.tag_errors import TagError
from app.models import NoteTag, NoteTagUpdate


def update_tag_by_id(tag_id: str, user_id: str, tag_update: NoteTagUpdate, tag_repository: TagRepository) -> Success[NoteTag] | Error[TagError]:
    tag = tag_repository.get_tag_by_id(tag_id, user_id)
    if tag is None:
        return Error(TagError.NOT_FOUND)
    
    # Check if new name already exists (if name is being updated)
    if tag_update.name and tag_update.name != tag.name:
        existing_tag = tag_repository.get_tag_by_name(tag_update.name, user_id)
        if existing_tag is not None:
            return Error(TagError.ALREADY_EXISTS)
    
    # Update fields
    update_data = tag_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(tag, field, value)
    
    updated_tag = tag_repository.update_tag(tag)
    return Success(updated_tag)