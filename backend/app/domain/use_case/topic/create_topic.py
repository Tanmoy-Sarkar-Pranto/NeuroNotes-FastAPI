from app.data.repository import TopicRepository, TopicEdgeRepository
from app.models import TopicCreate, User, Topic, TopicEdge
from app.core.domain import Success, Error
from app.domain.models import TopicError
from uuid import UUID


def create_topic(topic: TopicCreate, user: User, topic_repository: TopicRepository, topic_edge_repository: TopicEdgeRepository = None):
    topic_data = topic.model_dump(exclude={'related_topics', 'relation_types'})
    db_topic = Topic(**topic_data, user_id=user.id)

    topic_result = topic_repository.create_topic(db_topic)

    if isinstance(topic_result, Error):
        return topic_result

    created_topic = topic_result.data

    if not topic.related_topics or not topic_edge_repository:
        return topic_result

    if topic.related_topics:
        relation_types = topic.relation_types or []
        created_edges = []

        for i, target_topic_id in enumerate(topic.related_topics):
            relation_type = relation_types[i] if i < len(relation_types) else None

            edge = TopicEdge(
                source=created_topic.id,
                target=UUID(str(target_topic_id)),
                relation_type=relation_type
            )

            edge_result = topic_edge_repository.create_edge(edge)
            if isinstance(edge_result, Success):
                created_edges.append(edge_result.data)

    return topic_result
