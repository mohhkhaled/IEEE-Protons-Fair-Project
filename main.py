from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.staticfiles import StaticFiles 
from fastapi.responses import FileResponse
from typing import List
from sqlalchemy.orm import Session

# Import engine and get_db from your database.py module
from database import Base, engine, get_db
import models
import crud
import schemas

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# Create database tables
Base.metadata.create_all(bind=engine)


# --- HTML Page Routes ---

@app.get("/")
def read_root():
    return FileResponse("static/login.html")

@app.get("/register")
def read_register():
    return FileResponse("static/register.html")

@app.get("/dashboard")
def read_dashboard():
    return FileResponse("static/index.html")


# --- Announcements Endpoints ---

@app.post(
    "/announcements/",
    response_model=schemas.AnnouncementResponse,
    status_code=status.HTTP_201_CREATED
)
def add_announcement(data: schemas.AnnouncementCreate, db: Session = Depends(get_db)):
    return crud.create_announcement(db=db, data=data)

@app.get("/announcements/school/{school_id}", response_model=List[schemas.AnnouncementResponse])
def list_school_announcements(school_id: int, db: Session = Depends(get_db)):
    return crud.get_announcements_by_school(db=db, school_id=school_id)

@app.get("/announcements/{announcement_id}", response_model=schemas.AnnouncementResponse)
def get_announcement(announcement_id: int, db: Session = Depends(get_db)):
    announcement = crud.get_announcement_by_id(db=db, announcement_id=announcement_id)
    if not announcement:
        raise HTTPException(status_code=404, detail="Announcement not found")
    return announcement

@app.delete("/announcements/{announcement_id}")
def remove_announcement(announcement_id: int, db: Session = Depends(get_db)):
    success = crud.delete_announcement(db=db, announcement_id=announcement_id)
    if not success:
        raise HTTPException(status_code=404, detail="Announcement not found")
    return {"message": "Announcement deleted successfully"}


# --- Documents Endpoints ---

@app.post("/documents/", response_model=schemas.DocumentResponse, status_code=status.HTTP_201_CREATED)
def add_document(data: schemas.DocumentCreate, db: Session = Depends(get_db)):
    return crud.create_document(db=db, data=data)

@app.get(
    "/documents/school/{school_id}",
    response_model=List[schemas.DocumentResponse]
)
def list_documents(school_id: int, db: Session = Depends(get_db)):
    return crud.get_documents_by_school(db=db, school_id=school_id)

@app.get(
    "/documents/{document_id}",
    response_model=schemas.DocumentResponse
)
def get_document(document_id: int, db: Session = Depends(get_db)):
    doc = crud.get_document_by_id(db=db, document_id=document_id)
    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    return doc

@app.delete("/documents/{document_id}")
def remove_document(document_id: int, uploader_id: int, db: Session = Depends(get_db)):
    success = crud.delete_document(db=db, document_id=document_id, uploader_id=uploader_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Document not found or permission denied"
        )
    return {"message": "Document deleted successfully"}