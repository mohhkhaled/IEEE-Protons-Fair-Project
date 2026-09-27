from fastapi import FastAPI

# Assuming your teammates built these as APIRouters instead of Blueprints:
# from students import router as students_router
# from teachers import router as teachers_router

app = FastAPI(title="School Website API", version="1.0")
from database import engine, Base
import models  # Imports your models so SQLAlchemy knows they exist

# This creates the tables in MySQL automatically if they don't exist yet
Base.metadata.create_all(bind=engine)

# Register routers (FastAPI's version of app.register_blueprint)
# app.include_router(students_router, prefix="/students", tags=["Students"])
# app.include_router(teachers_router, prefix="/teachers", tags=["Teachers"])

@app.get("/")
def root():
    return {"message": "School Website API is running 🚀"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)