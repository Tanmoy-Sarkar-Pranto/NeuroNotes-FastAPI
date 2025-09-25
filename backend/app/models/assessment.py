from typing_extensions import TYPE_CHECKING
from sqlmodel import SQLModel
from uuid import UUID, uuid4
from sqlmodel import Field

if TYPE_CHECKING:
    from app.models import User


# class AssessmentBase(SQLModel):
#     topics = Topic


class Assessment(SQLModel):
    __tablename__: str = "assessments"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", index=True, ondelete="CASCADE")
