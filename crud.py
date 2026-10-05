"""
crud.py
Functions that actually talk to the database.
Routes in main.py will call these instead of writing
database queries directly.
"""
from database import SessionLocal
from models import Documents, Notifications, Schools

def create_document(uploader_id: int, school_id: int, file_name: str, file_path: str):
    session = SessionLocal()
    new_doc = Documents(
        uploader_id=uploader_id,
        school_id=school_id,
        file_name=file_name,
        file_path=file_path
    )
    session.add(new_doc)
    session.commit()
    session.refresh(new_doc)
    session.close()
    return new_doc


def get_documents_by_school(school_id: int):
    session = SessionLocal()
    results = (
        session.query(Documents)
        .filter(Documents.school_id == school_id)
        .order_by(Documents.uploaded_at.desc())
        .all()
    )
    session.close()
    return results


def get_document_by_id(document_id: int):
    session = SessionLocal()
    result = session.query(Documents).filter(Documents.id == document_id).first()
    session.close()
    return result


def delete_document(document_id: int, uploader_id: int):
    session = SessionLocal()
    doc = (
        session.query(Documents)
        .filter(Documents.id == document_id, Documents.uploader_id == uploader_id)
        .first()
    )
    if doc:
        session.delete(doc)
        session.commit()
        session.close()
        return True
    session.close()
    return False



def add_notification(user_id, message, notif_type):
    """Add a new notification"""
    session = SessionLocal()
    new_notification = Notifications(
        user_id=user_id,
        message=message,
        type=notif_type,
        is_read=False
    )
    session.add(new_notification)
    session.commit()
    session.close()

def get_user_notifications(user_id):
    """Get all notifications for a specific user"""
    session = SessionLocal()
    results = session.query(Notifications).filter(Notifications.user_id == user_id).all()
    session.close()
    return results
def get_unread_notifications(user_id):
    """Get only unread notifications for a specific user"""
    session = SessionLocal()
    results = session.query(Notifications).filter(
        Notifications.user_id == user_id,
        Notifications.is_read.is_(False)
    ).all()
    session.close()
    return results

def mark_as_read(notification_id):
    """Mark a notification as read"""
    session = SessionLocal()
    notification = session.query(Notifications).filter(Notifications.id == notification_id).first()
    if notification:
        notification.is_read = True
        session.commit()
    session.close()

def delete_notification(notification_id):
    """Delete a specific notification"""
    session = SessionLocal()
    notification = session.query(Notifications).filter(Notifications.id == notification_id).first()
    if notification:
        session.delete(notification)
        session.commit()
    session.close()

def add_school(name, logo_url=None):
    """Add a new school"""
    session = SessionLocal()
    new_school = Schools(
        name=name,
        logo_url=logo_url
    )
    session.add(new_school)
    session.commit()
    session.close()


def get_all_schools():
    """Get all schools"""
    session = SessionLocal()
    results = session.query(Schools).all()
    session.close()
    return results


def get_school_by_id(school_id):
    """Get a specific school by its id"""
    session = SessionLocal()
    result = session.query(Schools).filter(Schools.id == school_id).first()
    session.close()
    return result


def update_school(school_id, name=None, logo_url=None):
    """Update a school's name or logo"""
    session = SessionLocal()
    school = session.query(Schools).filter(Schools.id == school_id).first()
    if school:
        if name:
            school.name = name
        if logo_url:
            school.logo_url = logo_url
        session.commit()
    session.close()


def delete_school(school_id):
    """Delete a school"""
    session = SessionLocal()
    school = session.query(Schools).filter(Schools.id == school_id).first()
    if school:
        session.delete(school)
        session.commit()
    session.close()
