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
    national_id = Column(String(14), unique=True,index=True, nullable=False)
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
    is_read = Column(bool, default=False)  
#Announcements table for storing announcements
class Announcements(Base):
    __tablename__ = "announcements"

    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.id"))
    title = Column(String(255))
    content = Column(String(255))
    created_at = Column(String(255))

#Documents table for storing documents
class Documents(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    uploader_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    school_id = Column(Integer, nullable=False)
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)