from app.core.domain import Success, Error
from app.data.repository import TopicRepository
from app.domain.models import TopicError
from app.models import TopicRead


def read_topic_by_id(user_id: str, topic_id: str, topic_repository: TopicRepository) -> Success[TopicRead] | Error[TopicError]:
    topic = topic_repository.get_topic_by_id(topic_id, user_id)
    if topic is None:
        return Error(TopicError.NOT_FOUND)

    topic_read = TopicRead(**topic.model_dump())

    return Success(topic_read)