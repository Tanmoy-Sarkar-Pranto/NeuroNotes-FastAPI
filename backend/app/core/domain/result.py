from dataclasses import dataclass
from typing import Generic, TypeVar

D = TypeVar("D")
E = TypeVar("E")


@dataclass
class Success(Generic[D]):
    data: D


@dataclass
class Error(Generic[E]):
    error: E