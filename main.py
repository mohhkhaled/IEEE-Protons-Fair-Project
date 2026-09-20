from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, Base, Engine
from models import Assignments
from crud import (
    create_document, get_documents_by_school, get_document_by_id, delete_document,
    create_announcement, get_announcements_by_school, get_announcement_by_id,
    update_announcement, delete_announcement
)
from pydantic import BaseModel
from typing import Optional

Base.metadata.create_all(bind=Engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class AnnouncementUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


# ANNOUNCEMENTS APIs
@app.post("/announcements")
def add_announcement(school_id: int, title: str, content: str):
    return create_announcement(school_id, title, content)


@app.get("/announcements/school/{school_id}")
def list_announcements(school_id: int):
    return get_announcements_by_school(school_id)


@app.get("/announcements/{announcement_id}")
def get_announcement(announcement_id: int):
    announcement = get_announcement_by_id(announcement_id)
    if not announcement:
        return {"error": "Announcement not found"}
    return announcement


@app.put("/announcements/{announcement_id}")
def edit_announcement(announcement_id: int, announcement: AnnouncementUpdate):
    updated = update_announcement(announcement_id, announcement.title, announcement.content)
    if not updated:
        return {"error": "Announcement not found"}
    return updated


@app.delete("/announcements/{announcement_id}")
def remove_announcement(announcement_id: int):
    success = delete_announcement(announcement_id)
    if not success:
        return {"error": "Announcement not found"}
    return {"message": "Announcement deleted"}


# ASSIGNMENTS APIs
@app.get("/assignments")
def read_assignments(db: Session = Depends(get_db)):
    return db.query(Assignments).all()


@app.post("/assignments")
def create_assignment(title: str, description: str, due_date: str, school_id: int, db: Session = Depends(get_db)):
    new_assignment = Assignments(
        title=title,
        description=description,
        due_date=due_date,
        school_id=school_id
    )
    db.add(new_assignment)
    db.commit()
    db.refresh(new_assignment)
    return new_assignment


# DOCUMENTS APIs
@app.post("/documents/")
def add_document(uploader_id: int, school_id: int, file_name: str, file_path: str):
    return create_document(uploader_id, school_id, file_name, file_path)


@app.get("/documents/school/{school_id}")
def list_documents(school_id: int):
    return get_documents_by_school(school_id)


@app.get("/documents/{document_id}")
def get_document(document_id: int):
    doc = get_document_by_id(document_id)
    if not doc:
        return {"error": "Document not found"}
    return doc


@app.delete("/documents/{document_id}")
def remove_document(document_id: int, uploader_id: int):
    success = delete_document(document_id, uploader_id)
    if not success:
        return {"error": "Document not found or you don't have permission"}
    return {"message": "Document deleted"}