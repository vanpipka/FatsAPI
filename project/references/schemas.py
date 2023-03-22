from typing import List, Optional
from datetime import datetime

from pydantic import BaseModel, validator

import project.locations.schemas as locations_schemas


class _UserBase(BaseModel):
    name: str
    email: str


class UserCreate(_UserBase):
    password: str


class User(_UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True


class _VesselBase(BaseModel):
    name: str
    imo: str


class VesselCreate(_VesselBase):
    pass


class Vessel(_VesselBase):

    id: int
    mmsi: str
    marine_traffic_id: str
    country: Optional[locations_schemas.Country]

    class Config:
        orm_mode = True


class VesselList(Vessel):

    area: str
    country_code: str
    refresh_date: datetime

    class Config:
        orm_mode = True


class _ContainerBase(BaseModel):
    name: str


class ContainerCreate(_ContainerBase):
    pass


class Container(_ContainerBase):

    id: int
    routes: List[locations_schemas.Route]

    class Config:
        orm_mode = True

