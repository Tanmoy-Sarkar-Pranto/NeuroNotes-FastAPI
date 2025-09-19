from datetime import datetime
from uuid import UUID

from app.core.domain import Success, Error
from app.data.repository import TopicRepository, TopicEdgeRepository
from app.domain.models import TopicError
from app.models import TopicUpdate, TopicRead, Topic, TopicEdge


def update_topic_by_id(topic_id: str, user_id: str, topic: TopicUpdate, topic_repository: TopicRepository, topic_edge_repository: TopicEdgeRepository = None) -> Success[TopicRead] | Error[TopicError]:
    existing_topic = topic_repository.get_topic_by_id(topic_id, user_id)
    if existing_topic is None:
        return Error(TopicError.NOT_FOUND)

    existing_topic.title = topic.title or existing_topic.title
    existing_topic.description = topic.description or existing_topic.description
    existing_topic.updated_at = datetime.now()
    existing_topic.node_type = topic.node_type or existing_topic.node_type
    if topic.position is not None:
        existing_topic.position = topic.position

    updated_topic: Topic = topic_repository.update_topic(existing_topic)

    if topic.related_topics is not None and topic_edge_repository is not None:
        topic_edge_repository.delete_outgoing_edges_for_topic(topic_id)

        if topic.related_topics:
            relation_types = topic.relation_types or []

            for i, target_topic_id in enumerate(topic.related_topics):
                relation_type = relation_types[i] if i < len(relation_types) else None

                edge = TopicEdge(
                    source=UUID(topic_id),
                    target=UUID(str(target_topic_id)),
                    relation_type=relation_type
                )

                topic_edge_repository.create_edge(edge)

    return Success(TopicRead(
        id=updated_topic.id,
        title=updated_topic.title,
        description=updated_topic.description,
        node_type=updated_topic.node_type,
        position=updated_topic.position,
        created_at=updated_topic.created_at,
        updated_at=updated_topic.updated_at,
        user_id=updated_topic.user_id
    ))

