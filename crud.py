from database import SessionLocal
from models import Notification

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
