from datetime import datetime

from app.core.domain import Success, Error
from app.data.repository import TopicRepository
from app.domain.models import TopicError
from app.models import TopicUpdate, TopicRead, Topic


def update_topic_by_id(topic_id: str, user_id: str, topic: TopicUpdate, topic_repository: TopicRepository) -> Success[TopicRead] | Error[TopicError]:
    existing_topic = topic_repository.get_topic_by_id(topic_id, user_id)
    if existing_topic is None:
        return Error(TopicError.NOT_FOUND)

    existing_topic.title = topic.title or existing_topic.title
    existing_topic.description = topic.description or existing_topic.description
    existing_topic.updated_at = datetime.now()
    existing_topic.node_type = topic.node_type or existing_topic.node_type
    if topic.position is not None:
        existing_topic.position = topic.position

    topic: Topic = topic_repository.update_topic(existing_topic)

    return Success(TopicRead(**topic.model_dump()))

