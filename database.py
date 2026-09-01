from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base
#Database connection URL for MySQL database using mysqlconnector driver
DATABASE_URL = "mysql+mysqlconnector://root:PASSWORD@localhost/NAME"
#Object Relational Mapping (ORM) for database connection and table creation
Engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=Engine)
Base = declarative_base()
#Main table for users
class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nationalId = Column(String(14), unique=True,index=True )
    name = Column(String(255))
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255))
    role = Column(String(10))
#Student table
class Students(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    userId = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    grade = Column(String(50))
#Teachers table
class Teachers(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True, index=True)
    userId = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    subject = Column(String(255))

