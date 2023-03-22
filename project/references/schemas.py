from typing import List, Optional
from datetime import datetime

from pydantic import BaseModel


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

    # import project.locations.schemas as locations_schema

    id: int
    mmsi: str
    marine_traffic_id: str
    # country: Optional[locations_schema.Country]

    class Config:
        orm_mode = True


class VesselList(Vessel):

    area: str
    refresh_date: datetime

    class Config:
        orm_mode = True


class _ContainerBase(BaseModel):
    name: str


class ContainerCreate(_ContainerBase):
    pass


class Container(_ContainerBase):
    from project.locations.schemas import Route as RouteSchema

    id: int
    routes: List[RouteSchema]

    class Config:
        orm_mode = True

