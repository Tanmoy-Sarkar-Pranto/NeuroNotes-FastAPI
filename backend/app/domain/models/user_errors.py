from enum import Enum, auto


class UserError(Enum):
    NOT_FOUND = auto()
    UNAUTHORIZED = auto()
    ALREADY_EXISTS = auto()
    INVALID_CREDENTIALS = auto()
