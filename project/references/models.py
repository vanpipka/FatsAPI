from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from project.database import Base


class User(Base):
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


class Vessel(Base):

    from project.locations.models import Coordinate

    __tablename__ = "vessels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, default="")
    imo = Column(String, unique=True, index=True, default="")
    mmsi = Column(String, default="")

    coordinates = relationship("Coordinate", back_populates="vessel")

    def __init__(self, name, imo, *args, **kwargs):
        self.name = name
        self.imo = imo
