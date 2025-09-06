from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.core import get_session, create_access_token
from app.dtos import UserApiResponse
from app.models import UserLogin, User, UserLoginResponse, UserCreate, UserRead
from app.util import verify_password, hash_password

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)

@router.post("/register", response_model=UserApiResponse[UserLoginResponse], response_model_exclude_none=True)
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    existing_user = session.exec(select(User).where(User.email == user.email)).first()
    if existing_user is not None:
        raise HTTPException(status_code=400, detail="User already exists with that email")
    try:
        user = UserCreate.model_dump(user)

        raw_password = user.pop("password")
        hashed_password = hash_password(raw_password)

        db_user = User(**user, hashed_password=hashed_password)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)

        user_response = UserRead(
            id=str(db_user.id),
            username=db_user.username,
            email=db_user.email,
            created_at=db_user.created_at
        )

        return UserApiResponse.success_response(message="User created successfully", data=user_response, status=201).model_dump()
    except RuntimeError as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=UserApiResponse[UserLoginResponse], response_model_exclude_none=True)
def login(user: UserLogin, session: Session = Depends(get_session)):
    email, password = user.email, user.password
    db_user = session.exec(select(User).where(User.email == email)).first()
    if db_user is not None:
        if verify_password(password, db_user.hashed_password):
            jwt_token = create_access_token({
                "userId": str(db_user.id),
                "username": db_user.username,
                "email": db_user.email,
            })
            user_login_response: UserLoginResponse = UserLoginResponse(
                id=str(db_user.id),
                username=db_user.username,
                email=db_user.email,
                access_token=jwt_token,
                token_type="Bearer",
                created_at=db_user.created_at,
            )
            return UserApiResponse.success_response(message="Login successfully", data=user_login_response).model_dump()
    return UserApiResponse.error_response(message="Invalid credentials", status=401).model_dump()