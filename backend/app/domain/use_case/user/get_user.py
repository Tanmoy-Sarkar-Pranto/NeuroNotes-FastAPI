from app.core.domain import Error, Success
from app.data.repository import UserRepository
from app.domain.models import UserError
from app.models import User


def get_user(decoded_token : dict, user_repository: UserRepository) -> Success[User] | Error[UserError]:
    user_id = decoded_token.get("userId")
    user = user_repository.get_user_by_id(user_id)
    if user is None:
        return Error(UserError.NOT_FOUND)

    return Success(user)