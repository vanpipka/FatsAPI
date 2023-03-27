from fastapi import Depends
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from project.database import Base
from project.common.models import ReferenceMixin
# import project.locations.models as locations_models


class User(Base, ReferenceMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String, default="")
    phone = Column(String, default="")
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    def __init__(self, name, email, hashed_password, *args, **kwargs):
        self.name = name
        self.email = email
        self.hashed_password = hashed_password


class Vessel(Base, ReferenceMixin):

    __tablename__ = "vessels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, default="")
    imo = Column(String, unique=True, index=True, default="")
    mmsi = Column(String, default="")
    marine_traffic_id = Column(String, default="")
    country_id = Column(Integer, ForeignKey("countries.id"))

    coordinates = relationship("Coordinate", back_populates="vessel")
    country = relationship("Country", back_populates="vessel")

    def __init__(self, name, imo, *args, **kwargs):
        self.name = name
        self.imo = imo


class Container(Base, ReferenceMixin):

    __tablename__ = "containers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, default="")

    routes = relationship("Route", back_populates="container")

    def __init__(self, name, *args, **kwargs):
        self.name = name
