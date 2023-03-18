from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from project.database import Base


class Coordinate(Base):
    __tablename__ = "coordinates"

    id = Column(Integer, primary_key=True, index=True)
    vessel_id = Column(Integer, ForeignKey("vessels.id"))
    latitude = Column(String, default="")
    longitude = Column(String, default="")
    date = Column(DateTime)

    vessel = relationship("Vessel", back_populates="coordinates")

    def __init__(self, vessel_id, date, latitude, longitude, *args, **kwargs):
        self.vessel_id = vessel_id
        self.date = date
        self.longitude = longitude
        self.latitude = latitude


