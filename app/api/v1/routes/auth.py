from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.core import get_session
from app.models import UserLogin, User
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
            return {"message": "Login successful"}
    return {"message": "Login unsuccessful"}