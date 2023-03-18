from pydantic import BaseModel
from datetime import datetime


class _CoordinateBase(BaseModel):

    latitude: str
    longitude: str
    date: datetime
    vessel_id: int


class CoordinateCreate(_CoordinateBase):
    pass


class Coordinate(_CoordinateBase):
    id: int

    class Config:
        orm_mode = True


class _VesselBase(BaseModel):

    name: str
    imo: str


class Vessel(_VesselBase):
    id: int
    mmsi: str

    class Config:
        orm_mode = True
