from app.core.domain import Success, Error
from app.data.repository import TopicRepository
from app.domain.models import TopicError


def delete_topic_by_id(topic_id: str, user_id: str, topic_repository: TopicRepository) -> Success[bool] | Error[TopicError]:
    topic = topic_repository.delete_topic(topic_id, user_id)
    if not topic:
        return Error(TopicError.NOT_FOUND)
    return Success(True)