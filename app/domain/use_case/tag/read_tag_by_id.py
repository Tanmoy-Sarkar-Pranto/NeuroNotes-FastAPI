from app.core.domain import Success, Error
from app.data.repository.tag import TagRepository
from app.domain.models.tag_errors import TagError
from app.models import NoteTag


def read_tag_by_id(tag_id: str, user_id: str, tag_repository: TagRepository) -> Success[NoteTag] | Error[TagError]:
    tag = tag_repository.get_tag_by_id(tag_id, user_id)
    if tag is None:
        return Error(TagError.NOT_FOUND)
    return Success(tag)