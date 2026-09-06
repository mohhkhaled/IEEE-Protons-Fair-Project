from pydantic import BaseModel, EmailStr
from datetime import datetime, date


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
    created_at: datetime

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
    sent_at: datetime
    is_read: bool

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
    created_at: datetime

    class Config:
        from_attributes = True


# =========================
# Documents
# =========================

class DocumentResponse(BaseModel):
    id: int
    uploader_id: int
    school_id: int
    file_name: str
    file_path: str
    uploaded_at: datetime

    class Config:
        from_attributes = True

