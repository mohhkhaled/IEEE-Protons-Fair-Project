import sqlalchemy 
from sqlalchemy.orm import sessionmaker, declarative_base
#Database connection URL for MySQL database using mysqlconnector driver
DATABASE_URL = "mysql+mysqlconnector://root:PASSWORD@localhost/NAME"
#Object Relational Mapping (ORM) for database connection and table creation
Engine = sqlalchemy.create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=Engine)
Base = declarative_base()
#Main table for users
class Users(Base):
    __tablename__ = "users"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)
    national_id = sqlalchemy.Column(sqlalchemy.String(14), unique=True,index=True )
    name = sqlalchemy.Column(sqlalchemy.String(255))
    email = sqlalchemy.Column(sqlalchemy.String(255), unique=True, index=True)
    password_hash = sqlalchemy.Column(sqlalchemy.String(255))
    role = sqlalchemy.Column(sqlalchemy.String(10))
    school_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("schools.id"))
    created_at = sqlalchemy.Column(sqlalchemy.String(255))
#Messages table for storing messages
class Messages(Base):
    __tablename__ = "messages"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)
    sender_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    receiver_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    content = sqlalchemy.Column(sqlalchemy.String(255))
    sent_at = sqlalchemy.Column(sqlalchemy.String(255))
    is_read = sqlalchemy.Column(sqlalchemy.Integer, default=0)  # 0 for unread, 1 for read
# Announcements table
class Announcements(Base):
    __tablename__ = "announcements"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)
    school_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("schools.id"))
    title = sqlalchemy.Column(sqlalchemy.String(255))
    content = sqlalchemy.Column(sqlalchemy.String(255))
    created_at = sqlalchemy.Column(sqlalchemy.String(255))
    