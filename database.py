from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
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
    created_at = Column(String(255))
#Messages table for storing messages
class Messages(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"))
    receiver_id = Column(Integer, ForeignKey("users.id"))
    content = Column(String(255))
    sent_at = Column(String(255))
    is_read = Column("Bool", default=False)  # 0 for unread, 1 for read

class Announcements(Base):
    __tablename__ = "announcements"

    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.id"))
    title = Column(String(255))
    content = Column(String(255))
    created_at = Column(String(255))

#Documents table
class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    uploaderId = Column(Integer, ForeignKey("users.id"), nullable=False)
    schoolId = Column(Integer, nullable=False)
    fileName = Column(String(255), nullable=False)
    filePath = Column(String(500), nullable=False)
    uploadedAt = Column(DateTime, default=datetime.utcnow)

class Assignments(Base):
    __tablename__ = "assignments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255))
    description = Column(String(500))
    status = Column(String(20))
    due_date = Column("Date", nullable=False)
    
class Notifications(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    message = Column(String(255))
    type = Column(String(50))
    is_read = Column(bool, default=False) 
    created_at = Column(String(255))
    
def add_notification(user_id, message, notif_type):
    """Add a new notification"""
    session = SessionLocal()
    new_notification = Notifications(
        user_id=user_id,
        message=message,
        type=notif_type,
        is_read=0
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
        Notifications.is_read == 0
    ).all()
    session.close()
    return results

def mark_as_read(notification_id):
    """Mark a notification as read"""
    session = SessionLocal()
    notification = session.query(Notifications).filter(Notifications.id == notification_id).first()
    if notification:
        notification.is_read = 1
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
class Schools(Base):
    __tablename__ = "schools"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    logo_url = Column(String(255))


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