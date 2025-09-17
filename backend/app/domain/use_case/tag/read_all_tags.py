from typing import List

from app.core.domain import Success, Error
from app.data.repository.tag import TagRepository
from app.domain.models.tag_errors import TagError
from app.models import NoteTag


def read_all_tags_by_user(user_id: str, tag_repository: TagRepository) -> Success[List[NoteTag]] | Error[TagError]:
    tags = tag_repository.get_all_tags_by_user(user_id)
    if not tags:
        return Error(TagError.EMPTY)
    return Success(tags)