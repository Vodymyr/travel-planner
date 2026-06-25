from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import (
    PlaceCreate,
    PlaceUpdate,
    PlaceResponse,
)

from app.crud_places import (
    add_place_to_project,
    get_project_places,
    get_project_place,
    update_place,
)

router = APIRouter(
    prefix="/projects",
    tags=["Places"]
)


@router.post(
    "/{project_id}/places",
    response_model=PlaceResponse,
    status_code=201
)
def create_place(
    project_id: int,
    place: PlaceCreate,
    db: Session = Depends(get_db)
):
    try:
        db_place = add_place_to_project(
            db,
            project_id,
            place
        )

        if db_place is None:
            raise HTTPException(
                status_code=404,
                detail="Project not found"
            )

        return db_place

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.get(
    "/{project_id}/places",
    response_model=list[PlaceResponse]
)
def read_places(
    project_id: int,
    db: Session = Depends(get_db)
):
    return get_project_places(db, project_id)


@router.get(
    "/{project_id}/places/{place_id}",
    response_model=PlaceResponse
)
def read_place(
    project_id: int,
    place_id: int,
    db: Session = Depends(get_db)
):
    place = get_project_place(
        db,
        project_id,
        place_id
    )

    if not place:
        raise HTTPException(
            status_code=404,
            detail="Place not found"
        )

    return place


@router.put(
    "/{project_id}/places/{place_id}",
    response_model=PlaceResponse
)
def edit_place(
    project_id: int,
    place_id: int,
    place_data: PlaceUpdate,
    db: Session = Depends(get_db)
):
    place = update_place(
        db,
        project_id,
        place_id,
        place_data
    )

    if not place:
        raise HTTPException(
            status_code=404,
            detail="Place not found"
        )

    return place