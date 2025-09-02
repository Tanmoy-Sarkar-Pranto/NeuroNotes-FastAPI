from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.core import get_session, create_access_token
from app.models import UserLogin, User, UserLoginResponse
from app.util import verify_password

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}}
)

@router.post("/login")
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
            return {"message": "Login successful", "data": user_login_response}
    return {"message": "Login unsuccessful"}