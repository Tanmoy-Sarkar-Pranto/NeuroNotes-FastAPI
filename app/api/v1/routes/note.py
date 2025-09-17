from typing import List

from fastapi import APIRouter, Depends

from app.core.deps import get_user_repository, get_note_repository, verify_token, get_topic_repository
from app.core.domain import Error
from app.data.repository import UserRepository, NoteRepository, TopicRepository
from app.domain.models import UserError, TopicError
from app.domain.models.note_errors import NoteError
from app.domain.use_case.note import read_all_notes_by_topic_id, create_new_note, read_note_by_id, update_note_by_id, delete_note_by_id
from app.domain.use_case.topic import read_topic_by_id
from app.domain.use_case.user.get_user import get_user
from app.dtos import NoteApiResponse
from app.models import Note, NoteCreate, NoteRead, NoteUpdate

router = APIRouter(
    prefix="/notes",
    tags=["note"],
    responses={404: {"description": "Not found"}}
)

@router.get("/{topicId}", response_model=NoteApiResponse[List[Note]], response_model_exclude_none=True)
def read_all_notes(topicId: str, decoded_token : dict = Depends(verify_token), note_repository: NoteRepository = Depends(get_note_repository), user_repository: UserRepository = Depends(get_user_repository), topic_repository: TopicRepository = Depends(get_topic_repository)):
    db_user = get_user(decoded_token, user_repository)
    if isinstance(db_user, Error):
        if db_user.error == UserError.NOT_FOUND:
            return NoteApiResponse.error_response(message="Unauthorized.", status=401).model_dump()

    db_topic = read_topic_by_id(str(db_user.data.id), topicId, topic_repository)
    if isinstance(db_topic, Error):
        if db_topic.error == TopicError.NOT_FOUND:
            return NoteApiResponse.error_response(message="Topic not found.", status=404).model_dump()

    result = read_all_notes_by_topic_id(topicId, str(db_user.data.id), note_repository)
    if isinstance(result, Error):
        if result.error == NoteError.NOT_FOUND:
            return NoteApiResponse.error_response(message="Notes not found.", status=404).model_dump()
    return NoteApiResponse.success_response(message="Notes fetched successfully.", data=result.data).model_dump()

@router.post("/", response_model=NoteApiResponse[NoteRead], response_model_exclude_none=True)
def create_note(note: NoteCreate, decoded_token : dict = Depends(verify_token), note_repository: NoteRepository = Depends(get_note_repository), user_repository: UserRepository = Depends(get_user_repository), topic_repository: TopicRepository = Depends(get_topic_repository)):
    db_user = get_user(decoded_token, user_repository)
    if isinstance(db_user, Error):
        if db_user.error == UserError.NOT_FOUND:
            return NoteApiResponse.error_response(message="Unauthorized.", status=401).model_dump()

    db_topic = read_topic_by_id(str(db_user.data.id), str(note.topic_id), topic_repository)
    if isinstance(db_topic, Error):
        if db_topic.error == TopicError.NOT_FOUND:
            return NoteApiResponse.error_response(message="Topic not found.", status=404).model_dump()

    result = create_new_note(note, str(db_user.data.id), note_repository)
    return NoteApiResponse.success_response(message="Note created successfully.", data=result.data).model_dump()

@router.get("/single/{noteid}", response_model=NoteApiResponse[NoteRead], response_model_exclude_none=True)
def read_note(noteid: str, decoded_token: dict = Depends(verify_token), note_repository: NoteRepository = Depends(get_note_repository), user_repository: UserRepository = Depends(get_user_repository)):
    db_user = get_user(decoded_token, user_repository)
    if isinstance(db_user, Error):
        if db_user.error == UserError.NOT_FOUND:
            return NoteApiResponse.error_response(message="Unauthorized.", status=401).model_dump()

    result = read_note_by_id(noteid, str(db_user.data.id), note_repository)
    if isinstance(result, Error):
        if result.error == NoteError.NOT_FOUND:
            return NoteApiResponse.error_response(message="Note not found.", status=404).model_dump()
    
    return NoteApiResponse.success_response(message="Note fetched successfully.", data=result.data).model_dump()

@router.patch("/{noteid}", response_model=NoteApiResponse[NoteRead], response_model_exclude_none=True)
def update_note(noteid: str, note: NoteUpdate, decoded_token: dict = Depends(verify_token), note_repository: NoteRepository = Depends(get_note_repository), user_repository: UserRepository = Depends(get_user_repository)):
    db_user = get_user(decoded_token, user_repository)
    if isinstance(db_user, Error):
        if db_user.error == UserError.NOT_FOUND:
            return NoteApiResponse.error_response(message="Unauthorized.", status=401).model_dump()

    result = update_note_by_id(noteid, str(db_user.data.id), note, note_repository)
    if isinstance(result, Error):
        if result.error == NoteError.NOT_FOUND:
            return NoteApiResponse.error_response(message="Note not found.", status=404).model_dump()
    
    return NoteApiResponse.success_response(message="Note updated successfully.", data=result.data).model_dump()

@router.delete("/{noteid}", response_model=NoteApiResponse[bool], response_model_exclude_none=True)
def delete_note(noteid: str, decoded_token: dict = Depends(verify_token), note_repository: NoteRepository = Depends(get_note_repository), user_repository: UserRepository = Depends(get_user_repository)):
    db_user = get_user(decoded_token, user_repository)
    if isinstance(db_user, Error):
        if db_user.error == UserError.NOT_FOUND:
            return NoteApiResponse.error_response(message="Unauthorized.", status=401).model_dump()

    result = delete_note_by_id(noteid, str(db_user.data.id), note_repository)
    if isinstance(result, Error):
        if result.error == NoteError.NOT_FOUND:
            return NoteApiResponse.error_response(message="Note not found.", status=404).model_dump()
    
    return NoteApiResponse.success_response(message="Note deleted successfully.", data=result.data, status=204).model_dump()