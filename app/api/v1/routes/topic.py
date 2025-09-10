from typing import List

from fastapi import APIRouter
from fastapi.params import Depends
from sqlmodel import Session

from app.core import get_session
from app.core.deps import get_topic_repository, verify_token, get_user_repository, get_current_user
from app.core.domain import Error
from app.data.repository import TopicRepository, UserRepository
from app.domain.models import TopicError, UserError
from app.domain.use_case.topic.read_all_topics import read_all_topics
from app.domain.use_case.user.get_user import get_user
from app.dtos import TopicApiResponse
from app.models import TopicCreate, TopicRead, User

from app.domain.use_case.topic import create_topic as create_topic_use_case

router = APIRouter(
    prefix="/topics",
    tags=["topic"],
    responses={404: {"description": "Not found"}}
)

@router.post("/", response_model=TopicApiResponse, response_model_exclude_none=True)
def create_topic(topic: TopicCreate, session: Session = Depends(get_session), decoded_token: dict = Depends(verify_token), topic_repository: TopicRepository = Depends(get_topic_repository), user_repository: UserRepository = Depends(get_user_repository)):
    db_user = get_user(decoded_token, user_repository)
    if isinstance(db_user, Error):
        if db_user.error == UserError.NOT_FOUND:
            return TopicApiResponse.error_response(message="User not found.").model_dump()

    result = create_topic_use_case(topic, db_user.data, topic_repository)
    if isinstance(result, Error):
        if result.error == TopicError.ALREADY_EXISTS:
            return TopicApiResponse.error_response(message="Topic already exists.").model_dump()
    return TopicApiResponse.success_response(message="Topic created successfully.", data=topic).model_dump()


@router.get("/", response_model=TopicApiResponse[List[TopicRead]], response_model_exclude_none=True)
def read_topics(decoded_token : dict = Depends(verify_token), topic_repository: TopicRepository = Depends(get_topic_repository), user_repository: UserRepository = Depends(get_user_repository)):
    db_user = get_user(decoded_token, user_repository)
    if isinstance(db_user, Error):
        if db_user.error == UserError.NOT_FOUND:
            return TopicApiResponse.error_response(message="User not found.").model_dump()

    result = read_all_topics(db_user.data, topic_repository)
    if isinstance(result, Error):
        if result.error == TopicError.EMPTY:
            return TopicApiResponse.error_response(message="No topics found.").model_dump()
    return TopicApiResponse.success_response(message="Topics fetched successfully.", data=result.data).model_dump()