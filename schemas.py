from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


# =========================
# Users
# =========================

class UserCreate(BaseModel):
    national_id: str
    name: str
    email: EmailStr
    password: str
    role: str
    school_id: int


class UserResponse(BaseModel):
    id: int
    national_id: str
    name: str
    email: EmailStr
    role: str
    school_id: int
    created_at: str

    class Config:
        from_attributes = True


# =========================
# Messages
# =========================

class MessageCreate(BaseModel):
    receiver_id: int
    content: str


class MessageResponse(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    content: str
    sent_at: str
    is_read: int

    class Config:
        from_attributes = True


# =========================
# Announcements
# =========================

class AnnouncementCreate(BaseModel):
    school_id: int
    title: str
    content: str


class AnnouncementResponse(BaseModel):
    id: int
    school_id: int
    title: str
    content: str
    created_at: str

    class Config:
        from_attributes = True


# =========================
# Documents
# =========================

class DocumentResponse(BaseModel):
    id: int
    uploaderId: int
    schoolId: int
    fileName: str
    filePath: str
    uploadedAt: datetime

    class Config:
        from_attributes = True