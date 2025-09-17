from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.core import get_session
from app.core.deps import get_user_repository, verify_token
from app.core.domain import Error
from app.data.repository import UserRepository
from app.domain.models import UserError
from app.domain.use_case.user.get_user import get_user
from app.dtos import UserApiResponse
from app.models import UserRead

router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}}
)

@router.get("/", response_model=UserApiResponse[UserRead], response_model_exclude_none=True)
async def read_user(session: Session = Depends(get_session), decoded_token: dict = Depends(verify_token), user_repository: UserRepository = Depends(get_user_repository)):
    result = get_user(decoded_token, user_repository)
    if isinstance(result, Error):
        if UserError.NOT_FOUND == result.error:
            return UserApiResponse.error_response(message="User not found.").model_dump()

    user_response = UserRead(
        id=str(result.data.id),
        username=result.data.username,
        email=result.data.email,
        created_at=result.data.created_at
    )

    return UserApiResponse.success_response(message="Fetched user successfully", data=user_response).model_dump()
