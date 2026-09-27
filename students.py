from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import Student
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/students", tags=["Students"])

# Pydantic schemas for request validation
class StudentCreate(BaseModel):
    full_name: str
    email: str
    grade: str
    phone: Optional[str] = None

class StudentUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    grade: Optional[str] = None
    phone: Optional[str] = None


# ---------- Create a New Student ----------
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_student(student_data: StudentCreate, db: Session = Depends(get_db)):
    db_student = Student(
        full_name=student_data.full_name,
        email=student_data.email,
        grade=student_data.grade,
        phone=student_data.phone
    )
    db.add(db_student)
    try:
        db.commit()
        db.refresh(db_student)
        return {"id": db_student.id, "message": "Student created successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


# ---------- Get All Students ----------
@router.get("/")
def get_students(db: Session = Depends(get_db)):
    students = db.query(Student).all()
    return students


# ---------- Get a Single Student ----------
@router.get("/{student_id}")
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


# ---------- Update a Student ----------
@router.put("/{student_id}")
def update_student(student_id: int, student_data: StudentUpdate, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Update only fields that were sent in the request
    update_data = student_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(student, key, value)
    
    try:
        db.commit()
        db.refresh(student)
        return {"message": "Student updated successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


# ---------- Delete a Student ----------
@router.delete("/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    db.delete(student)
    db.commit()
    return {"message": "Student deleted successfully"}