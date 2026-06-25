from sqlalchemy.orm import Session

from app.models import Project, Place
from app.schemas import ProjectCreate
from app.services.art_api import get_artwork


def create_project(db: Session, project_data: ProjectCreate):

    db_project = Project(
        name=project_data.name,
        description=project_data.description,
        start_date=project_data.start_date,
    )

    db.add(db_project)
    db.commit()
    db.refresh(db_project)

    for place in project_data.places:

        artwork = get_artwork(place.external_id)

        if artwork is None:
            continue

        db_place = Place(
            project_id=db_project.id,
            external_id=place.external_id,
            title=artwork["title"],
            notes=place.notes,
            visited=False
        )

        db.add(db_place)

    db.commit()

    return db_project