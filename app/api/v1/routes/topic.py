from fastapi import APIRouter
from fastapi.params import Depends
from sqlmodel import Session

from app.core import get_session
from app.core.deps import get_topic_repository, verify_token, get_user_repository
from app.core.domain import Error
from app.data.repository import TopicRepository, UserRepository
from app.domain.models import TopicError
from app.dtos import TopicApiResponse
from app.models import TopicCreate

from app.domain.use_case.topic import create_topic as create_topic_use_case

router = APIRouter(
    prefix="/topic",
    tags=["topic"],
    responses={404: {"description": "Not found"}}
)

@router.post("/", response_model=TopicApiResponse, response_model_exclude_none=True)
def create_topic(topic: TopicCreate, session: Session = Depends(get_session), decoded_token: str = Depends(verify_token), topic_repository: TopicRepository = Depends(get_topic_repository), user_repository: UserRepository = Depends(get_user_repository)):
    db_user = user_repository.get_user_by_id(decoded_token["userId"])
    if db_user is None:
        return TopicApiResponse.error_response(message="User not found.")
    result = create_topic_use_case(topic, db_user, topic_repository)
    if isinstance(result, Error):
        if result.error == TopicError.ALREADY_EXISTS:
            return TopicApiResponse.error_response(message="Topic already exists.").model_dump()
    return TopicApiResponse.success_response(message="Topic created successfully.", data=topic).model_dump()


