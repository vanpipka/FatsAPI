from sqlalchemy.orm import Session, aliased
from sqlalchemy import select, and_, literal_column, join, func, text

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 10, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "@salt"
    db_user = models.User(email=user.email, name=user.name, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def get_vessel(db: Session, vessel_id: int):
    return db.query(models.Vessel).filter(models.Vessel.id == vessel_id).first()


def get_vessel_by_imo(db: Session, vessel_imo: str):
    return db.query(models.Vessel).filter(models.Vessel.imo == vessel_imo).first()


def create_vessel(db: Session, vessel: schemas.VesselCreate):
    from .tasks import download_marine_traffic_vessel_id

    db_vessel = models.Vessel(name=vessel.name, imo=vessel.imo)
    db.add(db_vessel)
    db.commit()
    db.refresh(db_vessel)

    download_marine_traffic_vessel_id.delay(vessel.imo)

    return db_vessel


def get_vessels(db: Session, skip: int = 10, limit: int = 100):
    return db.query(models.Vessel).offset(skip).limit(limit).all()


def get_vessels_on_tracking(db: Session):
    return db.query(models.Vessel).filter(models.Vessel.marine_traffic_id != "").all()


def get_container(db: Session, container_id: int):
    return db.query(models.Container).filter(models.Container.id == container_id).first()


def create_container(db: Session, container: schemas.ContainerCreate):
    db_container = models.Container(name=container.name)
    db.add(db_container)
    db.commit()
    db.refresh(db_container)

    return db_container


def get_containers(db: Session, skip: int = 10, limit: int = 100):
    return db.query(models.Container).offset(skip).limit(limit).all()


def get_vessels_list(db: Session, skip: int = 10, limit: int = 100):
    from project.locations.models import Coordinate, Area
    from .query_texts import VESSELS_LIST

    vessels = get_vessels(db, skip, limit)

    vessels_ids = [i.id for i in vessels]

    data = list(db.execute(text(VESSELS_LIST)))

    for i in data:
        print(i.name)

    return data


def get_container_by_name(db: Session, name: str):
    return db.query(models.Container).filter(models.Container.name == name).first()
