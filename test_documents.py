from database import SessionLocal, Document

session = SessionLocal()

print("Inserting a test document...")

test_doc = Document(
    uploaderId=1,
    schoolId=1,
    fileName="test_homework.pdf",
    filePath="/uploads/documents/test_homework.pdf"
)

session.add(test_doc)
session.commit()

print(f"Inserted! New document id: {test_doc.id}")

print("\nReading it back from the database...")
result = session.query(Document).filter_by(id=test_doc.id).first()

if result:
    print(f"Found document: id={result.id}, fileName={result.fileName}, "
          f"uploaderId={result.uploaderId}, uploadedAt={result.uploadedAt}")
else:
    print("Something went wrong — document not found.")

print("\nCleaning up test data...")
session.delete(result)
session.commit()
print("Test document deleted.")

session.close()
print("\nDone. If you saw no errors above, the documents table works correctly.")