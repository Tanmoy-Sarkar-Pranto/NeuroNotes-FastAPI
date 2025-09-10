from typing import List

from app.core.domain import Success, Error
from app.data.repository import TopicRepository
from app.domain.models import TopicError
from app.models import User, TopicRead


def read_all_topics(user: User, topic_repository: TopicRepository) -> Success[List[TopicRead]] | Error[TopicError]:
    topics = topic_repository.get_all_topics(str(user.id))
    if len(topics) == 0:
        return Error(TopicError.EMPTY)

    topic_read_list = []
    for topic in topics:
        topic_read_list.append(TopicRead(**topic.model_dump()))
    return Success(topic_read_list)