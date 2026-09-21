from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database URL (SQLite)
SQLALCHEMY_DATABASE_URL = "sqlite:///./school.db"

# Create the engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Add get_db() right here at the bottom
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
