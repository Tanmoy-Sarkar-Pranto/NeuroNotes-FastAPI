from sqlmodel import select

from app.models import User


class UserRepository:
    def __init__(self, session):
        self.session = session

    def create_user(self, user: User):
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def get_user_by_email(self, email: str) -> User | None:
        user: User = self.session.exec(select(User).where(User.email == email)).first()
        return user