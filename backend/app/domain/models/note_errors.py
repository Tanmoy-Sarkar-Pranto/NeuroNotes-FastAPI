from enum import Enum, auto


class NoteError(Enum):
    NOT_FOUND = auto()
    ALREADY_EXISTS = auto()
    EMPTY = auto()
    INVALID_TAGS = auto()
