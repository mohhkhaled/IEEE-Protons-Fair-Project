from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import Assignments, SessionLocal, Announcements

app = FastAPI()

# Dependency to open and close the database session automatically
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
# 1. API endpoint to fetch all announcements (GET)
@app.get("/announcements")
def read_announcements(db: Session = Depends(get_db)):
    return db.query(Announcements).all()
# 2. API endpoint to create a new announcement (POST)
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
# Fetch all assignments (GET)
@app.get("/assignments")
def read_assignments(db: Session = Depends(get_db)):
    return db.query(Assignments).all()
# Create a new assignment (POST)
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
