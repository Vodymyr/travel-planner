from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app import crud
from app.models import Place
from app.schemas import PlaceCreate, PlaceUpdate
from app.services.art_api import get_artwork


def add_place_to_project(
    db: Session, project_id: int, place_data: PlaceCreate
) -> Place | None:

    db_project = crud.get_project(db, project_id)
    if not db_project:
        return None

    places_count = db.scalar(
        select(func.count())
        .select_from(Place)
        .where(Place.project_id == project_id)
    ) or 0

    if places_count >= 10:
        raise ValueError("уже достигнут лимит в 10 мест")

    duplicate_query = select(Place).where(
        Place.project_id == project_id, Place.external_id == place_data.external_id
    )
    if db.scalars(duplicate_query).first():
        raise ValueError(
            f"Artwork с id {place_data.external_id} уже добавлен"
        )

    artwork_info = get_artwork(place_data.external_id)
    if artwork_info is None:
        raise ValueError(
            f"Artwork {place_data.external_id} not found in Art Institute API"
        )

    title = artwork_info["title"]

    db_place = Place(
        project_id=project_id,
        external_id=place_data.external_id,
        title=title,
        notes=place_data.notes,
        visited=False,
    )

    db.add(db_place)
    db.commit()
    db.refresh(db_place)

    return db_place


def get_project_places(db: Session, project_id: int) -> list[Place]:
    query = select(Place).where(Place.project_id == project_id)
    return list(db.scalars(query).all())


def get_project_place(
    db: Session,
    project_id: int,
    place_id: int
) -> Place | None:

    query = select(Place).where(
        Place.project_id == project_id,
        Place.id == place_id
    )

    return db.scalars(query).first()


def check_project_completed(db: Session, project_id: int):

    project = crud.get_project(db, project_id)

    if not project:
        return

    places = get_project_places(db, project_id)

    if len(places) == 0:
        project.completed = False

    elif all(place.visited for place in places):
        project.completed = True

    else:
        project.completed = False

    db.commit()


def update_place(
    db: Session,
    project_id: int,
    place_id: int,
    place_data: PlaceUpdate
) -> Place | None:

    db_place = get_project_place(
        db,
        project_id,
        place_id
    )

    if not db_place:
        return None

    update_data = place_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_place, key, value)

    db.commit()
    db.refresh(db_place)

    check_project_completed(db, project_id)

    return db_place