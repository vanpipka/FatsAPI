import datetime as _dt

import pydantic as _pydantic


class _UserBase(_pydantic.BaseModel):
    email: str


class UserCreate(_UserBase):
    password: str


class User(_UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True


class Сoordinate(_pydantic.BaseModel):

    id: int
    latitude: str
    longitude: str
    name: str
    date: _dt.datetime
    description: str
    #container: "Container"


class _ContainerBase(_pydantic.BaseModel):
    name: str


class ContainerCreate(_ContainerBase):
    pass


class Container(_ContainerBase):

    id: int
    coordinates: list[Сoordinate]
    user: User

    class Config:
        orm_mode = True

