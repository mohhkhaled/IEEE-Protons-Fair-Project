from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Date, Boolean
from datetime import datetime
from sqlalchemy.orm import sessionmaker, declarative_base
#Database connection URL for MySQL database using mysqlconnector driver
DATABASE_URL = "mysql+mysqlconnector://root:253daleen2013@localhost/project"
#Object Relational Mapping (ORM) for database connection and table creation
Engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=Engine)
Base = declarative_base()
#Main table for users
class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    national_id = Column(String(14), unique=True,index=True )
    name = Column(String(255))
    email = Column(String(255), unique=True, index=True)
    password_hash = Column(String(255))
    role = Column(String(10))
    school_id = Column(Integer, ForeignKey("schools.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
#Messages table for storing messages
class Messages(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"))
    receiver_id = Column(Integer, ForeignKey("users.id"))
    content = Column(String(65536))
    sent_at = Column(DateTime, default=datetime.utcnow)
    is_read = Column(Boolean, default=False)  # 0 for unread, 1 for read

class Announcements(Base):
    __tablename__ = "announcements"

    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.id"))
    title = Column(String(220))
    content = Column(String(3000))
    created_at = Column(DateTime, default=datetime.utcnow)

#Documents table
class Documents(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    uploader_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

class Todos(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(220))
    description = Column(String(1500))
    status = Column(String(20), default="pending")
    due_date = Column(Date, nullable=False)

class Schools(Base):
    __tablename__ = "schools"

    id = Column(Integer,primary_key=True, index=True)
    logo_url = Column(String(255))
    name = Column(String(220))
class Notifications(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    message = Column(String(255))
    type = Column(String(50))
    is_read = Column(Boolean, default=False) 
    created_at = Column(DateTime, default=datetime.utcnow)
    
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
