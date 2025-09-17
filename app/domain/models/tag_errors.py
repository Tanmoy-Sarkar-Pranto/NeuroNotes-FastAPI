from enum import Enum, auto


class TagError(Enum):
    NOT_FOUND = auto()
    ALREADY_EXISTS = auto()
    EMPTY = auto()