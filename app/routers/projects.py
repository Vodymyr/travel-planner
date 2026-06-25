from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app import crud
from app.schemas import (
    ProjectCreate,
    ProjectUpdate,
    ProjectResponse
)

router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=ProjectResponse, status_code=201)
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db)
):
    return crud.create_project(db, project)


@router.get("/", response_model=list[ProjectResponse])
def get_projects(
    db: Session = Depends(get_db)
):
    return crud.get_projects(db)


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    project = crud.get_project(db, project_id)

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    return project


@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: int,
    project: ProjectUpdate,
    db: Session = Depends(get_db)
):
    updated = crud.update_project(
        db,
        project_id,
        project
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    return updated


@router.delete("/{project_id}")
def delete_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    result = crud.delete_project(db, project_id)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    if result is False:
        raise HTTPException(
            status_code=400,
            detail="Project has visited places"
        )

    return {
        "message": "Project deleted successfully"
    }