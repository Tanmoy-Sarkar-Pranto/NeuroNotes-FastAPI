from typing import List

from sqlalchemy.exc import IntegrityError
from sqlmodel import select
from app.core.domain import Success, Error
from app.domain.models import TopicError
from app.models import Topic

class TopicRepository:
    def __init__(self, session):
        self.session = session

    def create_topic(self, topic: Topic) -> Success[Topic] | Error[TopicError]:
        try:
            self.session.add(topic)
            self.session.commit()
            self.session.refresh(topic)
        except IntegrityError as e:
            return Error(TopicError.ALREADY_EXISTS)

        return Success(topic)

    def get_topic_by_id(self, topic_id: int) -> Topic | None:
        topic: Topic = self.session.exec(select(Topic).where(Topic.id == topic_id)).first()
        return topic

    def get_all_topics(self, user_id: str) -> List[Topic] | None:
        topics: List[Topic] = self.session.exec(select(Topic).where(Topic.user_id == user_id)).all()
        return topics