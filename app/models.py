from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.database import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    start_date = Column(Date, nullable=True)
    completed = Column(Boolean, default=False)

    places = relationship(
        "Place",
        back_populates="project",
        cascade="all, delete-orphan"
    )


class Place(Base):
    __tablename__ = "places"

    id = Column(Integer, primary_key=True, index=True)

    project_id = Column(
        Integer,
        ForeignKey("projects.id"),
        nullable=False
    )

    external_id = Column(Integer, nullable=False)
    title = Column(String(255), nullable=False)

    notes = Column(Text, nullable=True)
    visited = Column(Boolean, default=False)

    project = relationship(
        "Project",
        back_populates="places"
    )