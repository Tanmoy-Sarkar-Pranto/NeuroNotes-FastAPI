from uuid import UUID
from typing import List, Optional

from sqlmodel import select

from app.models import NoteTag, NoteTagCreate, NoteTagUpdate


class TagRepository:
    def __init__(self, session):
        self.session = session

    def create_tag(self, tag: NoteTag) -> NoteTag:
        self.session.add(tag)
        self.session.commit()
        self.session.refresh(tag)
        return tag

    def get_tag_by_id(self, tag_id: str, user_id: str) -> Optional[NoteTag]:
        tag_uuid = UUID(tag_id)
        user_uuid = UUID(user_id)
        tag: NoteTag = self.session.exec(
            select(NoteTag).where(
                NoteTag.id == tag_uuid,
                NoteTag.user_id == user_uuid
            )
        ).first()
        return tag

    def get_tag_by_name(self, name: str, user_id: str) -> Optional[NoteTag]:
        user_uuid = UUID(user_id)
        tag: NoteTag = self.session.exec(
            select(NoteTag).where(
                NoteTag.name == name,
                NoteTag.user_id == user_uuid
            )
        ).first()
        return tag

    def get_all_tags_by_user(self, user_id: str) -> List[NoteTag]:
        user_uuid = UUID(user_id)
        tags = self.session.exec(
            select(NoteTag).where(NoteTag.user_id == user_uuid)
        ).all()
        return list(tags)

    def update_tag(self, tag: NoteTag) -> NoteTag:
        self.session.add(tag)
        self.session.commit()
        self.session.refresh(tag)
        return tag

    def delete_tag(self, tag: NoteTag) -> bool:
        self.session.delete(tag)
        self.session.commit()
        return True