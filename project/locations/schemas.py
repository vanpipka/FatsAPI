from pydantic import BaseModel
from datetime import datetime


class _CoordinateBase(BaseModel):

    latitude: str
    longitude: str
    date: datetime
    vessel_id: int
    area: str


class CoordinateCreate(_CoordinateBase):
    pass


class Coordinate(_CoordinateBase):
    id: int

    class Config:
        orm_mode = True


class _RouteBase(BaseModel):

    container_id: int
    start_place: str
    start_date: datetime
    end_place: str
    end_date: datetime


class RouteCreate(_RouteBase):
    pass


class Route(_RouteBase):
    id: int

    class Config:
        orm_mode = True


class _CountryBase(BaseModel):

    name: str
    code: str


class \
        CountryCreate(_CountryBase):
    pass


class Country(_CountryBase):
    id: int

    class Config:
        orm_mode = True
