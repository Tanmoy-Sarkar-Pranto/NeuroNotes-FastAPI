from typing import List
from uuid import UUID

from sqlmodel import select

from app.models import Note, NoteTag, NoteTagMap, NoteReadWithTags, NoteTagRead


class NoteRepository:
    def __init__(self, session):
        self.session = session

    def create_note(self, note: Note) -> Note:
        self.session.add(note)
        self.session.commit()
        self.session.refresh(note)
        return note

    def read_all_notes(self, topic_id: str, user_id: str) -> List[Note] | None:
        notes: List[Note] = self.session.exec(select(Note).where(Note.user_id == user_id, Note.topic_id == topic_id)).all()
        return notes

    def read_note_by_id(self, note_id: str, user_id: str) -> Note | None:
        note: Note = self.session.exec(select(Note).where(Note.id == note_id, Note.user_id == user_id)).first()
        return note

    def update_note(self, note: Note) -> Note | None:
        self.session.add(note)
        self.session.commit()
        self.session.refresh(note)
        return note

    def delete_note(self, note_id: str, user_id: str) -> bool:
        note: Note = self.session.exec(select(Note).where(Note.id == note_id, Note.user_id == user_id)).first()
        if note is None:
            return False
        self.session.delete(note)
        self.session.commit()
        return True

    def validate_tags_belong_to_user(self, tag_ids: List[UUID], user_id: str) -> bool:
        """Validate that all provided tag IDs exist and belong to the user"""
        if not tag_ids:
            return True
        
        user_uuid = UUID(user_id)
        existing_tags = self.session.exec(
            select(NoteTag).where(
                NoteTag.id.in_(tag_ids),
                NoteTag.user_id == user_uuid
            )
        ).all()
        
        return len(existing_tags) == len(tag_ids)

    def set_note_tags(self, note_id: UUID, tag_ids: List[UUID]) -> None:
        """Set tags for a note (clears existing tags and sets new ones)"""
        # Clear existing tag associations
        existing_associations = self.session.exec(
            select(NoteTagMap).where(NoteTagMap.note_id == note_id)
        ).all()
        
        for association in existing_associations:
            self.session.delete(association)
        
        # Add new tag associations
        for tag_id in tag_ids:
            association = NoteTagMap(note_id=note_id, tag_id=tag_id)
            self.session.add(association)
        
        self.session.commit()

    def get_note_tags(self, note_id: UUID) -> List[NoteTag]:
        """Get all tags associated with a note"""
        tags = self.session.exec(
            select(NoteTag)
            .join(NoteTagMap, NoteTag.id == NoteTagMap.tag_id)
            .where(NoteTagMap.note_id == note_id)
        ).all()
        
        return list(tags)

    def read_note_with_tags(self, note_id: str, user_id: str) -> NoteReadWithTags | None:
        """Read a note and include its associated tags"""
        note = self.read_note_by_id(note_id, user_id)
        if note is None:
            return None
        
        tags = self.get_note_tags(note.id)
        tag_reads = [NoteTagRead(**tag.model_dump()) for tag in tags]
        
        # Create NoteReadWithTags explicitly
        return NoteReadWithTags(
            id=note.id,
            topic_id=note.topic_id,
            title=note.title,
            content=note.content,
            urls=note.urls,
            created_at=note.created_at,
            updated_at=note.updated_at,
            tags=tag_reads
        )

    def read_all_notes_with_tags(self, topic_id: str, user_id: str) -> List[NoteReadWithTags]:
        """Read all notes for a topic and include their associated tags"""
        notes = self.read_all_notes(topic_id, user_id)
        if not notes:
            return []
        
        result = []
        for note in notes:
            tags = self.get_note_tags(note.id)
            tag_reads = [NoteTagRead(**tag.model_dump()) for tag in tags]
            
            note_with_tags = NoteReadWithTags(
                id=note.id,
                topic_id=note.topic_id,
                title=note.title,
                content=note.content,
                urls=note.urls,
                created_at=note.created_at,
                updated_at=note.updated_at,
                tags=tag_reads
            )
            result.append(note_with_tags)
        
        return result
