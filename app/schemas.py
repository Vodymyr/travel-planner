from datetime import date
from typing import Optional

from pydantic import BaseModel


class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: Optional[date] = None

    places: list[PlaceCreate] = []


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[date] = None


class ProjectResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    start_date: Optional[date] = None
    completed: bool

    model_config = {
        "from_attributes": True
    }


class PlaceCreate(BaseModel):
    external_id: int
    notes: Optional[str] = None


class PlaceUpdate(BaseModel):
    notes: Optional[str] = None
    visited: Optional[bool] = None


class PlaceResponse(BaseModel):
    id: int
    project_id: int
    external_id: int
    title: str
    notes: Optional[str] = None
    visited: bool

    model_config = {
        "from_attributes": True
    }