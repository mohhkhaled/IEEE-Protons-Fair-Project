from fastapi import FastAPI 
from fastapi.staticfiles import StaticFiles 
from fastapi.responses import FileResponse
from database import Base, Engine
import models
import crud
from crud import *
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"),name="static")

Base.metadata.create_all(bind=Engine)


@app.get("/")
def read_root():
    return FileResponse("static/login.html")

@app.get("/register")
def read_register():
    return FileResponse("static/register.html")

@app.get("/dashboard")
def read_dashboard():
    return FileResponse("static/index.html")

@app.post("/documents/")
def add_document(uploader_id: int, school_id: int, file_name: str, file_path: str):
    return create_document(uploader_id, school_id, file_name, file_path)

@app.get("/documents/school/{school_id}")
def list_documents(school_id: int):
    return get_documents_by_school(school_id)

@app.get("/documents/{document_id}")
def get_document(document_id: int):
    doc = get_document_by_id(document_id)
    if not doc:
        return {"error": "Document not found"}
    return doc

@app.delete("/documents/{document_id}")
def remove_document(document_id: int, uploader_id: int):
    success = delete_document(document_id, uploader_id)
    if not success:
        return {"error": "Document not found or you don't have permission"}
    return {"message": "Document deleted"}