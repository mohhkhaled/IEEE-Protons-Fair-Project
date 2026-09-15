from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, Announcements, Assignments, Base, Engine
import models
from crud import create_document, get_documents_by_school, get_document_by_id, delete_document

Base.metadata.create_all(bind=Engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ANNOUNCEMENTS APIs
@app.get("/announcements")
def read_announcements(db: Session = Depends(get_db)):
    return db.query(Announcements).all()

@app.post("/announcements")
def create_announcement(title: str, content: str, school_id: int, created_at: str, db: Session = Depends(get_db)):
    new_announcement = Announcements(
        title=title,
        content=content,
        school_id=school_id,
        created_at=created_at
    )
    db.add(new_announcement)
    db.commit()
    db.refresh(new_announcement)
    return new_announcement

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