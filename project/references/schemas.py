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
    id: int
    mmsi: str

    class Config:
        orm_mode = True
