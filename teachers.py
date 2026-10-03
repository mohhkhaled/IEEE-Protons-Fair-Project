from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import Teacher
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/teachers", tags=["Teachers"])

# Pydantic schemas for request validation
class TeacherCreate(BaseModel):
    full_name: str
    email: str
    phone: Optional[str] = None
    department: Optional[str] = None

class TeacherUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    department: Optional[str] = None


# ---------- Create a New Teacher ----------
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_teacher(teacher_data: TeacherCreate, db: Session = Depends(get_db)):
    db_teacher = Teacher(
        full_name=teacher_data.full_name,
        email=teacher_data.email,
        phone=teacher_data.phone,
        department=teacher_data.department
    )
    db.add(db_teacher)
    try:
        db.commit()
        db.refresh(db_teacher)
        return {"id": db_teacher.id, "message": "Teacher created successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


# ---------- Get All Teachers ----------
@router.get("/")
def get_teachers(db: Session = Depends(get_db)):
    teachers = db.query(Teacher).all()
    return teachers


# ---------- Get a Single Teacher ----------
@router.get("/{teacher_id}")
def get_teacher(teacher_id: int, db: Session = Depends(get_db)):
    teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return teacher


# ---------- Update a Teacher ----------
@router.put("/{teacher_id}")
def update_teacher(teacher_id: int, teacher_data: TeacherUpdate, db: Session = Depends(get_db)):
    teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    update_data = teacher_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(teacher, key, value)
    
    try:
        db.commit()
        db.refresh(teacher)
        return {"message": "Teacher updated successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


# ---------- Delete a Teacher ----------
@router.delete("/{teacher_id}")
def delete_teacher(teacher_id: int, db: Session = Depends(get_db)):
    teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    db.delete(teacher)
    db.commit()
    return {"message": "Teacher deleted successfully"}