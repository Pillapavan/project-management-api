from fastapi import FastAPI
from app.database.connection import Base,engine
from app.routers import auth, users,projects,issues,comments
from app.logging_config import setup_logging

setup_logging()
app = FastAPI(    title="Project Management API",
    version="1.0.0")

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(projects.router)
app.include_router(issues.router)
app.include_router(comments.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Project Management API!"}