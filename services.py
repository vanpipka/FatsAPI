import sqlalchemy.orm as _orm

import models as _models
import schemas as _schemas
import database as _database


def create_database():
    return _database.Base.metadata.create_all(bind=_database.engine)


def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_user(db: _orm.Session, user: _schemas.UserCreate):

    fake_hashed_password = user.password + "@salt"
    db_user = _models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def get_user_by_email(db: _orm.Session, email: str):
    return db.query(_models.User).filter(_models.User.email == email).first()


def get_users(db: _orm.Session, skip: int = 10, limit: int = 100):
    return db.query(_models.User).offset(skip).limit(limit).all()


def get_user(db: _orm.Session, user_id: int):
    return db.query(_models.User).filter(_models.User.id == user_id).first()


def get_containers(db: _orm.Session, user_id: int, skip: int = 10, limit: int = 100):
    return db.query(_models.Container).filter(_models.User.id == user_id).offset(skip).limit(limit).all()


def create_container(db: _orm.Session, container: _schemas.ContainerCreate, user_id: int):

    container = _models.Container(name=container.name, user_id=user_id)
    db.add(container)
    db.commit()
    db.refresh(container)
    return container


def get_containers(db: _orm.Session, skip: int = 10, limit: int = 100):
    return db.query(_models.Container).offset(skip).limit(limit).all()


def get_containers_by_user(db: _orm.Session, user: _schemas.User):
    return db.query(_models.Container).filter(_models.Container.user == user).all()


def get_container(db: _orm.Session, container_id: int):
    return db.query(_models.Container).filter(_models.Container.id == container_id).first()
