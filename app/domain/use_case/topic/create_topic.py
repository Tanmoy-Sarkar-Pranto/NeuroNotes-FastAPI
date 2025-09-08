from app.data.repository import TopicRepository
from app.models import TopicCreate, User, Topic


def create_topic(topic: TopicCreate, user: User, topic_repository: TopicRepository):
    db_topic = Topic(**topic.model_dump(), user_id=user.id)
    return topic_repository.create_topic(db_topic)
