from typing import List
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlmodel import select
from app.core.domain import Success, Error
from app.domain.models import TopicEdgeError
from app.models import TopicEdge, Topic

class TopicEdgeRepository:
    def __init__(self, session):
        self.session = session

    def create_edge(self, edge: TopicEdge) -> Success[TopicEdge] | Error[TopicEdgeError]:
        try:
            source_topic = self.session.exec(select(Topic).where(Topic.id == edge.source)).first()
            target_topic = self.session.exec(select(Topic).where(Topic.id == edge.target)).first()

            if not source_topic or not target_topic:
                return Error(TopicEdgeError.INVALID_EDGE)

            if edge.source == edge.target:
                return Error(TopicEdgeError.INVALID_EDGE)

            existing_edge = self.session.exec(
                select(TopicEdge).where(
                    TopicEdge.source == edge.source,
                    TopicEdge.target == edge.target
                )
            ).first()

            if existing_edge:
                return Error(TopicEdgeError.ALREADY_EXISTS)

            self.session.add(edge)
            self.session.commit()
            self.session.refresh(edge)
        except IntegrityError:
            return Error(TopicEdgeError.ALREADY_EXISTS)

        return Success(edge)

    def get_edge_by_id(self, edge_id: str) -> TopicEdge | None:
        edge: TopicEdge = self.session.exec(select(TopicEdge).where(TopicEdge.id == edge_id)).first()
        return edge

    def get_edges_by_source(self, source_topic_id: str) -> List[TopicEdge]:
        edges: List[TopicEdge] = self.session.exec(
            select(TopicEdge).where(TopicEdge.source == source_topic_id)
        ).all()
        return edges

    def get_edges_by_target(self, target_topic_id: str) -> List[TopicEdge]:
        edges: List[TopicEdge] = self.session.exec(
            select(TopicEdge).where(TopicEdge.target == target_topic_id)
        ).all()
        return edges

    def get_all_edges_for_topic(self, topic_id: str) -> List[TopicEdge]:
        edges: List[TopicEdge] = self.session.exec(
            select(TopicEdge).where(
                (TopicEdge.source == topic_id) | (TopicEdge.target == topic_id)
            )
        ).all()
        return edges

    def get_edges_for_user(self, user_id: str) -> List[TopicEdge]:
        edges: List[TopicEdge] = self.session.exec(
            select(TopicEdge)
            .join(Topic, TopicEdge.source == Topic.id)
            .where(Topic.user_id == user_id)
        ).all()
        return edges

    def update_edge(self, edge: TopicEdge) -> TopicEdge | None:
        self.session.add(edge)
        self.session.commit()
        self.session.refresh(edge)
        return edge

    def delete_edge(self, edge_id: str) -> bool:
        edge: TopicEdge = self.session.exec(select(TopicEdge).where(TopicEdge.id == edge_id)).first()
        if edge is None:
            return False
        self.session.delete(edge)
        self.session.commit()
        return True

    def delete_edges_for_topic(self, topic_id: str) -> bool:
        edges = self.session.exec(
            select(TopicEdge).where(
                (TopicEdge.source == topic_id) | (TopicEdge.target == topic_id)
            )
        ).all()

        for edge in edges:
            self.session.delete(edge)

        self.session.commit()
        return True

    def delete_outgoing_edges_for_topic(self, topic_id: str) -> bool:
        edges = self.session.exec(
            select(TopicEdge).where(TopicEdge.source == topic_id)
        ).all()

        for edge in edges:
            self.session.delete(edge)

        self.session.commit()
        return True

    def delete_edge_by_source_target(self, source_id: str, target_id: str) -> bool:
        edge = self.session.exec(
            select(TopicEdge).where(
                (TopicEdge.source == source_id) & (TopicEdge.target == target_id)
            )
        ).first()

        if edge:
            self.session.delete(edge)
            self.session.commit()
            return True
        return False

    def create_multiple_edges(self, edges: List[TopicEdge]) -> Success[List[TopicEdge]] | Error[TopicEdgeError]:
        try:
            created_edges = []
            for edge in edges:
                source_topic = self.session.exec(select(Topic).where(Topic.id == edge.source)).first()
                target_topic = self.session.exec(select(Topic).where(Topic.id == edge.target)).first()

                if not source_topic or not target_topic:
                    return Error(TopicEdgeError.INVALID_EDGE)

                if edge.source == edge.target:
                    return Error(TopicEdgeError.INVALID_EDGE)

                existing_edge = self.session.exec(
                    select(TopicEdge).where(
                        TopicEdge.source == edge.source,
                        TopicEdge.target == edge.target
                    )
                ).first()

                if existing_edge:
                    continue

                self.session.add(edge)
                created_edges.append(edge)

            self.session.commit()

            for edge in created_edges:
                self.session.refresh(edge)

        except IntegrityError:
            return Error(TopicEdgeError.ALREADY_EXISTS)

        return Success(created_edges)