from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "mysql+mysqlconnector://root:PASSWORD@localhost/NAME"

Engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=Engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nationalId = Column(String(14), unique=True,index=True )
    name = Column(String(255))
    email = Column(String(255))
    password = Column(String(255))
    role = Column(String(10))

class Students(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    grade = Column(String(50))

class Teachers(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String(255))
    
