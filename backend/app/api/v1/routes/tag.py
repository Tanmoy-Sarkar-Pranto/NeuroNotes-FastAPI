from typing import List

from fastapi import APIRouter, Depends

from app.core.deps import get_user_repository, get_tag_repository, verify_token
from app.core.domain import Error
from app.data.repository import UserRepository
from app.data.repository.tag import TagRepository
from app.domain.models import UserError
from app.domain.models.tag_errors import TagError
from app.domain.use_case.tag import create_tag, read_all_tags_by_user, read_tag_by_id, update_tag_by_id, delete_tag_by_id
from app.domain.use_case.user.get_user import get_user
from app.dtos import TagApiResponse
from app.models import NoteTag, NoteTagCreate, NoteTagRead, NoteTagUpdate

router = APIRouter(
    prefix="/tags",
    tags=["tag"],
    responses={404: {"description": "Not found"}}
)

@router.post("/", response_model=TagApiResponse[NoteTagRead], response_model_exclude_none=True)
def create_new_tag(tag: NoteTagCreate, decoded_token: dict = Depends(verify_token), tag_repository: TagRepository = Depends(get_tag_repository), user_repository: UserRepository = Depends(get_user_repository)):
    db_user = get_user(decoded_token, user_repository)
    if isinstance(db_user, Error):
        if db_user.error == UserError.NOT_FOUND:
            return TagApiResponse.error_response(message="Unauthorized.", status=401).model_dump()

    result = create_tag(tag, str(db_user.data.id), tag_repository)
    if isinstance(result, Error):
        if result.error == TagError.ALREADY_EXISTS:
            return TagApiResponse.error_response(message="Tag already exists.", status=409).model_dump()
    
    return TagApiResponse.success_response(message="Tag created successfully.", data=result.data).model_dump()

@router.get("/", response_model=TagApiResponse[List[NoteTagRead]], response_model_exclude_none=True)
def read_all_tags(decoded_token: dict = Depends(verify_token), tag_repository: TagRepository = Depends(get_tag_repository), user_repository: UserRepository = Depends(get_user_repository)):
    db_user = get_user(decoded_token, user_repository)
    if isinstance(db_user, Error):
        if db_user.error == UserError.NOT_FOUND:
            return TagApiResponse.error_response(message="Unauthorized.", status=401).model_dump()

    result = read_all_tags_by_user(str(db_user.data.id), tag_repository)
    if isinstance(result, Error):
        if result.error == TagError.EMPTY:
            return TagApiResponse.error_response(message="No tags found.", status=404).model_dump()
    
    return TagApiResponse.success_response(message="Tags fetched successfully.", data=result.data).model_dump()

@router.get("/{tagid}", response_model=TagApiResponse[NoteTagRead], response_model_exclude_none=True)
def read_tag(tagid: str, decoded_token: dict = Depends(verify_token), tag_repository: TagRepository = Depends(get_tag_repository), user_repository: UserRepository = Depends(get_user_repository)):
    db_user = get_user(decoded_token, user_repository)
    if isinstance(db_user, Error):
        if db_user.error == UserError.NOT_FOUND:
            return TagApiResponse.error_response(message="Unauthorized.", status=401).model_dump()

    result = read_tag_by_id(tagid, str(db_user.data.id), tag_repository)
    if isinstance(result, Error):
        if result.error == TagError.NOT_FOUND:
            return TagApiResponse.error_response(message="Tag not found.", status=404).model_dump()
    
    return TagApiResponse.success_response(message="Tag fetched successfully.", data=result.data).model_dump()

@router.patch("/{tagid}", response_model=TagApiResponse[NoteTagRead], response_model_exclude_none=True)
def update_tag(tagid: str, tag: NoteTagUpdate, decoded_token: dict = Depends(verify_token), tag_repository: TagRepository = Depends(get_tag_repository), user_repository: UserRepository = Depends(get_user_repository)):
    db_user = get_user(decoded_token, user_repository)
    if isinstance(db_user, Error):
        if db_user.error == UserError.NOT_FOUND:
            return TagApiResponse.error_response(message="Unauthorized.", status=401).model_dump()

    result = update_tag_by_id(tagid, str(db_user.data.id), tag, tag_repository)
    if isinstance(result, Error):
        if result.error == TagError.NOT_FOUND:
            return TagApiResponse.error_response(message="Tag not found.", status=404).model_dump()
        elif result.error == TagError.ALREADY_EXISTS:
            return TagApiResponse.error_response(message="Tag name already exists.", status=409).model_dump()
    
    return TagApiResponse.success_response(message="Tag updated successfully.", data=result.data).model_dump()

@router.delete("/{tagid}", response_model=TagApiResponse[bool], response_model_exclude_none=True)
def delete_tag(tagid: str, decoded_token: dict = Depends(verify_token), tag_repository: TagRepository = Depends(get_tag_repository), user_repository: UserRepository = Depends(get_user_repository)):
    db_user = get_user(decoded_token, user_repository)
    if isinstance(db_user, Error):
        if db_user.error == UserError.NOT_FOUND:
            return TagApiResponse.error_response(message="Unauthorized.", status=401).model_dump()

    result = delete_tag_by_id(tagid, str(db_user.data.id), tag_repository)
    if isinstance(result, Error):
        if result.error == TagError.NOT_FOUND:
            return TagApiResponse.error_response(message="Tag not found.", status=404).model_dump()
    
    return TagApiResponse.success_response(message="Tag deleted successfully.", data=result.data, status=204).model_dump()