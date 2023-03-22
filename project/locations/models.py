from fastapi import Depends
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from project.database import Base

from project.models_utils import ReferenceMixin


class Country(Base, ReferenceMixin):

    __tablename__ = "countries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, default="")
    code = Column(String, default="")

    vessel = relationship("Vessel", back_populates="country")


class Area(Base, ReferenceMixin):
    __tablename__ = "areas"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, default="")

    coordinates = relationship("Coordinate", back_populates="area")


class Coordinate(Base, ReferenceMixin):
    __tablename__ = "coordinates"

    id = Column(Integer, primary_key=True, index=True)
    vessel_id = Column(Integer, ForeignKey("vessels.id"))
    area_id = Column(Integer, ForeignKey("areas.id"))
    latitude = Column(String, default="")
    longitude = Column(String, default="")
    date = Column(DateTime)

    vessel = relationship("Vessel", back_populates="coordinates")
    area = relationship("Area", back_populates="coordinates")

    def __init__(self, vessel_id, date, latitude, longitude, area_id, *args, **kwargs):
        self.vessel_id = vessel_id
        self.date = date
        self.longitude = longitude
        self.latitude = latitude
        self.area_id = area_id


class Route(Base, ReferenceMixin):
    __tablename__ = "routes"

    id = Column(Integer, primary_key=True, index=True)
    container_id = Column(Integer, ForeignKey("containers.id"))
    start_place = Column(String, default="")
    end_place = Column(String, default="")
    start_date = Column(DateTime, default="0001-01-01T01:01:01")
    end_date = Column(DateTime, default="0001-01-01T01:01:01")

    container = relationship("Container", back_populates="routes")

    def __init__(self, container_id, start_place, start_date, end_date, end_place,  *args, **kwargs):
        self.container_id = container_id
        self.start_place = start_place
        self.start_date = start_date
        self.end_place = end_place
        self.end_date = end_date




