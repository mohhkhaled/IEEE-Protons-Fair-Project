"""
crud.py
Functions that actually talk to the database.
Routes in main.py will call these instead of writing
database queries directly.
"""

from database import SessionLocal
from models import Documents


def create_document(uploader_id: int, school_id: int, file_name: str, file_path: str):
    session = SessionLocal()
    new_doc = Documents(
        uploader_id=uploader_id,
        school_id=school_id,
        file_name=file_name,
        file_path=file_path
    )
    session.add(new_doc)
    session.commit()
    session.refresh(new_doc)
    session.close()
    return new_doc


def get_documents_by_school(school_id: int):
    session = SessionLocal()
    results = (
        session.query(Documents)
        .filter(Documents.school_id == school_id)
        .order_by(Documents.uploaded_at.desc())
        .all()
    )
    session.close()
    return results


def get_document_by_id(document_id: int):
    session = SessionLocal()
    result = session.query(Documents).filter(Documents.id == document_id).first()
    session.close()
    return result


def delete_document(document_id: int, uploader_id: int):
    session = SessionLocal()
    doc = (
        session.query(Documents)
        .filter(Documents.id == document_id, Documents.uploader_id == uploader_id)
        .first()
    )
    if doc:
        session.delete(doc)
        session.commit()
        session.close()
        return True
    session.close()
    return False