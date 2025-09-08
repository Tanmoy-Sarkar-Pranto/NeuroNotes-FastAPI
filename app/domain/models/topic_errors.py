from enum import Enum, auto


class TopicError(Enum):
    NOT_FOUND = auto()
    UNAUTHORIZED = auto()
    ALREADY_EXISTS = auto()
