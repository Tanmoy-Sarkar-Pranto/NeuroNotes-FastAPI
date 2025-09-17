from sqlalchemy.exc import IntegrityError

from app.core.domain import Success, Error
from app.data.repository.tag import TagRepository
from app.domain.models.tag_errors import TagError
from app.models import NoteTag, NoteTagCreate


def create_tag(tag: NoteTagCreate, user_id: str, tag_repository: TagRepository) -> Success[NoteTag] | Error[TagError]:
    existing_tag = tag_repository.get_tag_by_name(tag.name, user_id)
    if existing_tag is not None:
        return Error(TagError.ALREADY_EXISTS)
    
    try:
        db_tag = NoteTag(**tag.model_dump(), user_id=user_id)
        created_tag = tag_repository.create_tag(db_tag)
        return Success(created_tag)
    except IntegrityError:
        return Error(TagError.ALREADY_EXISTS)