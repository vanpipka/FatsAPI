from sqlalchemy.orm import Session

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

    db_vessel = models.Vessel(name=vessel.name, imo=vessel.imo)
    db.add(db_vessel)
    db.commit()
    db.refresh(db_vessel)

    return db_vessel


def get_vessels(db: Session, skip: int = 10, limit: int = 100):
    return db.query(models.Vessel).offset(skip).limit(limit).all()
