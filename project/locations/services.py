from sqlalchemy.orm import Session

from . import models, schemas


def get_coordinates_for_vessel(db: Session, vessel_id: int):
    return db.query(models.Coordinate).filter(models.Coordinate.vessel_id == vessel_id).all()


def create_coordinate(db: Session, coordinate: schemas.CoordinateCreate):

    db_coordinate = get_coordinate_by_create_scheme(db, coordinate)

    if db_coordinate:
        return db_coordinate

    db_coordinate = models.Coordinate(
        vessel_id=coordinate.vessel_id,
        date=coordinate.date,
        longitude=coordinate.longitude,
        latitude=coordinate.latitude)

    db.add(db_coordinate)
    db.commit()
    db.refresh(db_coordinate)

    return db_coordinate


def get_coordinate_by_create_scheme(db: Session, coordinate: schemas.CoordinateCreate):

    return db.query(models.Coordinate).filter(models.Coordinate.vessel_id == coordinate.vessel_id
                                              and models.Coordinate.date == coordinate.date
                                              and models.Coordinate.longitude == coordinate.longitude
                                              and models.Coordinate.latitude == coordinate.latitude).first()


