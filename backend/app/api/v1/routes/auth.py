from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.core import get_session, create_access_token
from app.core.deps import get_user_repository
from app.core.domain import Error
from app.data.repository import UserRepository
from app.domain.models import UserError
from app.domain.use_case.auth import register_user
from app.domain.use_case.auth.login import login_user
from app.dtos import UserApiResponse
from app.models import UserLogin, UserLoginResponse, UserCreate, UserRead

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)

@router.post("/register", response_model=UserApiResponse[UserRead], response_model_exclude_none=True)
def create_user(user: UserCreate, session: Session = Depends(get_session), user_repository: UserRepository = Depends(get_user_repository)):
    result = register_user(user, user_repository)

    if isinstance(result, Error):
        if UserError.ALREADY_EXISTS == result.error:
            return UserApiResponse.error_response(message="User already exists with that email.").model_dump()

    user_response = UserRead(
        id=str(result.data.id),
        username=result.data.username,
        email=result.data.email,
        created_at=result.data.created_at
    )

    return UserApiResponse.success_response(message="User created successfully", data=user_response, status=201).model_dump()


@router.post("/login", response_model=UserApiResponse[UserLoginResponse], response_model_exclude_none=True)
def login(user: UserLogin, session: Session = Depends(get_session), user_repository: UserRepository = Depends(get_user_repository)):
    result = login_user(user, user_repository)
    if isinstance(result, Error):
        if UserError.INVALID_CREDENTIALS == result.error:
            return UserApiResponse.error_response(message="Invalid credentials", status=401).model_dump()

    jwt_token = create_access_token({
        "userId": str(result.data.id),
        "username": result.data.username,
        "email": result.data.email,
    })
    user_login_response: UserLoginResponse = UserLoginResponse(
        id=str(result.data.id),
        username=result.data.username,
        email=result.data.email,
        access_token=jwt_token,
        token_type="Bearer",
        created_at=result.data.created_at,
    )
    return UserApiResponse.success_response(message="Login successfully", data=user_login_response).model_dump()
