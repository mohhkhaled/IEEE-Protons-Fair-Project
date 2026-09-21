"""
crud.py
Functions that actually talk to the database.
Routes in main.py call these using the injected db session.
"""
from sqlalchemy.orm import Session
import models
import schemas


# --- Document CRUD Operations ---

def create_document(db: Session, data: schemas.DocumentCreate):
    new_doc = models.Documents(
        uploader_id=data.uploader_id,
        school_id=data.school_id,
        file_name=data.file_name,
        file_path=data.file_path
    )
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)
    return new_doc


def get_documents_by_school(db: Session, school_id: int):
    return (
        db.query(models.Documents)
        .filter(models.Documents.school_id == school_id)
        .order_by(models.Documents.uploaded_at.desc())
        .all()
    )


def get_document_by_id(db: Session, document_id: int):
    return db.query(models.Documents).filter(models.Documents.id == document_id).first()


def delete_document(db: Session, document_id: int, uploader_id: int):
    doc = (
        db.query(models.Documents)
        .filter(models.Documents.id == document_id, models.Documents.uploader_id == uploader_id)
        .first()
    )
    if doc:
        db.delete(doc)
        db.commit()
        return True
    return False


# --- Notification CRUD Operations ---

def add_notification(db: Session, user_id: int, message: str, notif_type: str):
    """Add a new notification"""
    new_notification = models.Notifications(
        user_id=user_id,
        message=message,
        type=notif_type,
        is_read=False
    )
    db.add(new_notification)
    db.commit()
    db.refresh(new_notification)
    return new_notification


def get_user_notifications(db: Session, user_id: int):
    """Get all notifications for a specific user"""
    return db.query(models.Notifications).filter(models.Notifications.user_id == user_id).all()


def get_unread_notifications(db: Session, user_id: int):
    """Get only unread notifications for a specific user"""
    return db.query(models.Notifications).filter(
        models.Notifications.user_id == user_id,
        models.Notifications.is_read.is_(False)
    ).all()


def mark_as_read(db: Session, notification_id: int):
    """Mark a notification as read"""
    notification = db.query(models.Notifications).filter(models.Notifications.id == notification_id).first()
    if notification:
        notification.is_read = True
        db.commit()
        return True
    return False


def delete_notification(db: Session, notification_id: int):
    """Delete a specific notification"""
    notification = db.query(models.Notifications).filter(models.Notifications.id == notification_id).first()
    if notification:
        db.delete(notification)
        db.commit()
        return True
    return False


# --- Announcements CRUD Operations ---

def create_announcement(db: Session, data: schemas.AnnouncementCreate):
    new_announcement = models.Announcements(
        school_id=data.school_id,
        title=data.title,
        content=data.content,
        category=data.category
    )
    db.add(new_announcement)
    db.commit()
    db.refresh(new_announcement)
    return new_announcement


def get_announcements_by_school(db: Session, school_id: int, limit: int = 20):
    return (
        db.query(models.Announcements)
        .filter(models.Announcements.school_id == school_id)
        .order_by(models.Announcements.created_at.desc())
        .limit(limit)
        .all()
    )


def get_announcement_by_id(db: Session, announcement_id: int):
    return (
        db.query(models.Announcements)
        .filter(models.Announcements.id == announcement_id)
        .first()
    )


def delete_announcement(db: Session, announcement_id: int):
    announcement = (
        db.query(models.Announcements)
        .filter(models.Announcements.id == announcement_id)
        .first()
    )
    if announcement:
        db.delete(announcement)
        db.commit()
        return True
    return False