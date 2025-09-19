from typing import List

from fastapi import APIRouter
from fastapi.params import Depends

from app.core.deps import get_topic_repository, get_topic_edge_repository, verify_token, get_user_repository
from app.core.domain import Error
from app.data.repository import TopicRepository, TopicEdgeRepository, UserRepository
from app.domain.models import TopicError, UserError, TopicEdgeError
from app.domain.use_case.topic import create_topic as create_topic_use_case, read_all_topics, read_topic_by_id, \
    update_topic_by_id, delete_topic_by_id
from app.domain.use_case.user.get_user import get_user
from app.dtos import TopicApiResponse
from app.models import TopicCreate, TopicRead, TopicUpdate, TopicEdge, TopicEdgeCreate

router = APIRouter(
    prefix="/topics",
    tags=["topic"],
    responses={404: {"description": "Not found"}}
)

@router.post("/", response_model=TopicApiResponse, response_model_exclude_none=True)
def create_topic(topic: TopicCreate, decoded_token: dict = Depends(verify_token), topic_repository: TopicRepository = Depends(get_topic_repository), topic_edge_repository: TopicEdgeRepository = Depends(get_topic_edge_repository), user_repository: UserRepository = Depends(get_user_repository)):
    db_user = get_user(decoded_token, user_repository)
    if isinstance(db_user, Error):
        if db_user.error == UserError.NOT_FOUND:
            return TopicApiResponse.error_response(message="Unauthorized.", status=401).model_dump()

    result = create_topic_use_case(topic, db_user.data, topic_repository, topic_edge_repository)
    if isinstance(result, Error):
        if result.error == TopicError.ALREADY_EXISTS:
            return TopicApiResponse.error_response(message="Topic already exists.").model_dump()
    return TopicApiResponse.success_response(message="Topic created successfully.", data=topic).model_dump()


@router.get("/", response_model=TopicApiResponse[List[TopicRead]], response_model_exclude_none=True)
def read_topics(decoded_token : dict = Depends(verify_token), topic_repository: TopicRepository = Depends(get_topic_repository), user_repository: UserRepository = Depends(get_user_repository)):
    db_user = get_user(decoded_token, user_repository)
    if isinstance(db_user, Error):
        if db_user.error == UserError.NOT_FOUND:
            return TopicApiResponse.error_response(message="Unauthorized.", status=401).model_dump()

    result = read_all_topics(db_user.data, topic_repository)
    if isinstance(result, Error):
        if result.error == TopicError.EMPTY:
            return TopicApiResponse.error_response(message="No topics found.", status=404).model_dump()
    return TopicApiResponse.success_response(message="Topics fetched successfully.", data=result.data).model_dump()

@router.get("/{topicid}", response_model=TopicApiResponse[TopicRead], response_model_exclude_none=True)
def read_topic(topicid: str, decoded_token : dict = Depends(verify_token), topic_repository: TopicRepository = Depends(get_topic_repository), user_repository: UserRepository = Depends(get_user_repository)):
    db_user = get_user(decoded_token, user_repository)
    if isinstance(db_user, Error):
        if db_user.error == UserError.NOT_FOUND:
            return TopicApiResponse.error_response(message="Unauthorized.", status=401).model_dump()

    result = read_topic_by_id(str(db_user.data.id) ,topicid, topic_repository)

    if isinstance(result, Error):
        if result.error == TopicError.NOT_FOUND:
            return TopicApiResponse.error_response(message="Topic not found.", status=404).model_dump()

    return TopicApiResponse.success_response(message="Topic fetched successfully.", data=result.data).model_dump()

@router.patch("/{topicid}", response_model=TopicApiResponse[TopicRead], response_model_exclude_none=True)
def update_topic(topicid: str, topic: TopicUpdate, decoded_token : dict = Depends(verify_token), topic_repository: TopicRepository = Depends(get_topic_repository), topic_edge_repository: TopicEdgeRepository = Depends(get_topic_edge_repository), user_repository: UserRepository = Depends(get_user_repository)):
    db_user = get_user(decoded_token, user_repository)
    if isinstance(db_user, Error):
        if db_user.error == UserError.NOT_FOUND:
            return TopicApiResponse.error_response(message="Unauthorized.", status=401).model_dump()

    result = update_topic_by_id(topicid, str(db_user.data.id), topic, topic_repository, topic_edge_repository)
    if isinstance(result, Error):
        if result.error == TopicError.NOT_FOUND:
            return TopicApiResponse.error_response(message="Topic not found.", status=404).model_dump()
    return TopicApiResponse.success_response(message="Topic updated successfully.", data=result.data).model_dump()

@router.get("/{topicid}/edges", response_model=TopicApiResponse, response_model_exclude_none=True)
def get_topic_edges(topicid: str, decoded_token: dict = Depends(verify_token), topic_edge_repository: TopicEdgeRepository = Depends(get_topic_edge_repository), user_repository: UserRepository = Depends(get_user_repository)):
    db_user = get_user(decoded_token, user_repository)
    if isinstance(db_user, Error):
        if db_user.error == UserError.NOT_FOUND:
            return TopicApiResponse.error_response(message="Unauthorized.", status=401).model_dump()

    edges = topic_edge_repository.get_edges_by_source(topicid)
    edge_data = []
    for edge in edges:
        edge_data.append({
            "target_topic_id": str(edge.target),
            "relation_type": edge.relation_type
        })

    return TopicApiResponse.success_response(message="Topic edges fetched successfully.", data=edge_data).model_dump()

@router.post("/topic-edges", response_model=TopicApiResponse, response_model_exclude_none=True)
def create_topic_edge(edge_data: TopicEdgeCreate, decoded_token: dict = Depends(verify_token), topic_edge_repository: TopicEdgeRepository = Depends(get_topic_edge_repository), user_repository: UserRepository = Depends(get_user_repository)):
    db_user = get_user(decoded_token, user_repository)
    if isinstance(db_user, Error):
        if db_user.error == UserError.NOT_FOUND:
            return TopicApiResponse.error_response(message="Unauthorized.", status=401).model_dump()

    # Create the edge
    edge = TopicEdge(
        source=edge_data.source,
        target=edge_data.target,
        relation_type=edge_data.relation_type
    )

    result = topic_edge_repository.create_edge(edge)
    if isinstance(result, Error):
        if result.error == TopicEdgeError.ALREADY_EXISTS:
            return TopicApiResponse.error_response(message="Edge already exists.", status=409).model_dump()
        elif result.error == TopicEdgeError.INVALID_EDGE:
            return TopicApiResponse.error_response(message="Invalid edge.", status=400).model_dump()
        else:
            return TopicApiResponse.error_response(message="Failed to create edge.", status=500).model_dump()

    return TopicApiResponse.success_response(message="Edge created successfully.", data=result.data).model_dump()

@router.delete("/topic-edges/{source_id}/{target_id}", response_model=TopicApiResponse, response_model_exclude_none=True)
def delete_topic_edge(source_id: str, target_id: str, decoded_token: dict = Depends(verify_token), topic_edge_repository: TopicEdgeRepository = Depends(get_topic_edge_repository), user_repository: UserRepository = Depends(get_user_repository)):
    db_user = get_user(decoded_token, user_repository)
    if isinstance(db_user, Error):
        if db_user.error == UserError.NOT_FOUND:
            return TopicApiResponse.error_response(message="Unauthorized.", status=401).model_dump()

    # Delete the edge
    result = topic_edge_repository.delete_edge_by_source_target(source_id, target_id)
    if not result:
        return TopicApiResponse.error_response(message="Edge not found.", status=404).model_dump()

    return TopicApiResponse.success_response(message="Edge deleted successfully.", data=True).model_dump()

@router.delete("/{topicid}", response_model=TopicApiResponse[bool], response_model_exclude_none=True)
def delete_topic(topicid: str, decoded_token : dict = Depends(verify_token), topic_repository: TopicRepository = Depends(get_topic_repository), user_repository: UserRepository = Depends(get_user_repository)):
    db_user = get_user(decoded_token, user_repository)
    if isinstance(db_user, Error):
        if db_user.error == UserError.NOT_FOUND:
            return TopicApiResponse.error_response(message="Unauthorized.", status=401).model_dump()

    result = delete_topic_by_id(topicid, str(db_user.data.id), topic_repository)
    if isinstance(result, Error):
        if result.error == TopicError.NOT_FOUND:
            return TopicApiResponse.error_response(message="Topic not found.", status=404).model_dump()
    return TopicApiResponse.success_response(message="Topic deleted successfully.", data=result.data, status=204).model_dump()