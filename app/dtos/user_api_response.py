from typing import Any, Optional, List, TypeVar, Generic
from pydantic import BaseModel, ConfigDict

# Generic type for data
T = TypeVar('T')


class ErrorDetail(BaseModel):
    field: str
    message: str


class UserApiResponse(BaseModel, Generic[T]):
    success: bool
    message: str
    data: Optional[T] = None
    status: int
    errors: Optional[List[ErrorDetail]] = None

    @classmethod
    def success_response(cls, message: str, data: T = None, status: int = 200) -> "UserApiResponse[T]":
        """Create a success response"""
        return cls(
            success=True,
            message=message,
            data=data,
            status=status
        )

    @classmethod
    def error_response(cls, message: str, errors: List[ErrorDetail] = None,status: int = 400) -> "UserApiResponse[None]":
        """Create an error response"""
        return cls(
            success=False,
            message=message,
            errors=errors or [],
            status=status
        )

