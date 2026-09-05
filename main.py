from fastapi import FastAPI
from database import Base, Engine

app = FastAPI()

Base.metadata.create_all(bind=Engine)