from enum import Enum, auto


class TopicEdgeError(Enum):
    NOT_FOUND = auto()
    UNAUTHORIZED = auto()
    ALREADY_EXISTS = auto()
    EMPTY = auto()
    INVALID_EDGE = auto()
    CIRCULAR_DEPENDENCY = auto()