from sqlalchemy.exc import IntegrityError

from app.core.domain import Success, Error
from app.data.repository import UserRepository
from app.domain.models import UserError
from app.models import User, UserCreate
from app.util import hash_password


def register_user(user: UserCreate, user_repository: UserRepository) -> Success[User] | Error[UserError]:
    existing_user = user_repository.get_user_by_email(user.email)
    if existing_user is not None:
        return Error(UserError.ALREADY_EXISTS)
    user = UserCreate.model_dump(user)
    try:

        raw_password = user.pop("password")
        hashed_password = hash_password(raw_password)

        db_user = User(**user, hashed_password=hashed_password)
        user_repository.create_user(db_user)
    except IntegrityError:
        return Error(UserError.ALREADY_EXISTS)
    return Success(db_user)
