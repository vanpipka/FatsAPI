from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import select

from . import models, schemas
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)


def get_coordinates_for_vessel(db: Session, vessel_id: int):
    return db.query(models.Coordinate).filter(models.Coordinate.vessel_id == vessel_id).all()


def get_last_coordinates(db: Session, containers: List["Vessel"]):
    pass


def create_coordinate(db: Session, coordinate: schemas.CoordinateCreate):

    db_coordinate = get_coordinate_by_create_scheme(db, coordinate)

    if db_coordinate:
        return db_coordinate

    area = get_or_create_area(db, area_name=coordinate.area)

    db_coordinate = models.Coordinate(
        vessel_id=coordinate.vessel_id,
        date=coordinate.date,
        longitude=coordinate.longitude,
        latitude=coordinate.latitude,
        area_id=area.id)

    db_coordinate.save(db)

    return db_coordinate


def get_coordinate_by_create_scheme(db: Session, coordinate: schemas.CoordinateCreate):

    return db.query(models.Coordinate).filter(models.Coordinate.vessel_id == coordinate.vessel_id,
                                              models.Coordinate.date == coordinate.date,
                                              models.Coordinate.longitude == coordinate.longitude,
                                              models.Coordinate.latitude == coordinate.latitude).first()


def get_routes_for_container(db: Session, container_id: int):
    return db.query(models.Route).filter(models.Route.container_id == container_id).all()


def create_route(db: Session, route: schemas.RouteCreate):

    db_route = models.Route(
        container_id=route.container_id,
        start_date=route.start_date,
        end_date=route.end_date,
        start_place=route.start_place,
        end_place=route.end_place)

    db_route.save(db)

    return db_route


def get_area_by_name(db: Session, area_name: str):
    return db.query(models.Area).filter(models.Area.name == area_name).first()


def get_or_create_area(db: Session, area_name: str):

    db_area = get_area_by_name(db, area_name=area_name)

    if db_area:
        return db_area

    db_area = models.Area(name=area_name)
    db_area.save(db)

    return db_area


def get_country_by_code(db: Session, country_code: str):
    return db.query(models.Country).filter(models.Country.code == country_code).first()


def get_or_create_country(db: Session, country: schemas.CountryCreate):

    db_country = get_country_by_code(db, country_code=country.code)

    if db_country:
        return db_country

    db_country = models.Country(name=country.name, code=country.code)
    db_country.save(db=db)

    return db_country

