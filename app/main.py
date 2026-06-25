from fastapi import FastAPI

from app.database import Base, engine
import app.models

from app.routers import projects
from app.routers import places

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Travel Planner API",
    version="1.0"
)

app.include_router(projects.router)
app.include_router(places.router)


@app.get("/")
def root():
    return {
        "message": "Travel Planner API"
    }