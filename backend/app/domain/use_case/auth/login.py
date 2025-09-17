from app.core.domain import Error, Success
from app.data.repository import UserRepository
from app.domain.models import UserError
from app.models import UserLogin, User
from app.util import verify_password


def login_user(user_login: UserLogin, user_repository: UserRepository) -> Success[User] | Error[UserError]:
    user = user_repository.get_user_by_email(user_login.email)
    if user is None:
        return Error(UserError.INVALID_CREDENTIALS)

    if not verify_password(user_login.password, user.hashed_password):
        return Error(UserError.INVALID_CREDENTIALS)

    return Success(user)