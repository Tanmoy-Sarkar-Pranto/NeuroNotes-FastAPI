from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session,select

from app.models import UserCreate, User, UserLogin
from app.core import get_session
from app.util import hash_password

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}}
)

@router.post("/")
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

        return {"message": "User created successfully"}
    except RuntimeError as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
