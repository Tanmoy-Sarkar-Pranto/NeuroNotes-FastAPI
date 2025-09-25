from fastapi import APIRouter

router = APIRouter(
    prefix="/ai-assessment",
    tags=["ai-assessment"],
    responses={404: {"description": "Not found"}}
)

