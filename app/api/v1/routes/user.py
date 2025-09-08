from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.core import get_session
from app.core.deps import get_user_repository, verify_token
from app.data.repository import UserRepository
from app.dtos import UserApiResponse
from app.models import UserRead

router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}}
)

@router.get("/", response_model=UserApiResponse[UserRead], response_model_exclude_none=True)
async def read_user(session: Session = Depends(get_session), decoded_token: str = Depends(verify_token), user_repository: UserRepository = Depends(get_user_repository)):
    db_user = user_repository.get_user_by_email(decoded_token["email"])

    if db_user is None:
        return UserApiResponse.error_response(message="User not found.")
    user_response = UserRead(
        id=str(db_user.id),
        username=db_user.username,
        email=db_user.email,
        created_at=db_user.created_at
    )

    return UserApiResponse.success_response(message="Fetched user successfully", data=user_response).model_dump()
