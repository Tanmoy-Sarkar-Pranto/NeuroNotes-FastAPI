from typing import List

from sqlmodel import select

from app.models import Note


class NoteRepository:
    def __init__(self, session):
        self.session = session

    def create_note(self, note: Note) -> Note:
        self.session.add(note)
        self.session.commit()
        self.session.refresh(note)
        return note

    def read_all_notes(self, user_id: str) -> List[Note] | None:
        notes: List[Note] = self.session.exec(select(Note).where(Note.user_id == user_id)).all()
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
