import logging
import random
from string import ascii_lowercase
from typing import List

from celery.result import AsyncResult
from fastapi import Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from . import references_router
from project.database import get_db_session

from . import schemas, services


@references_router.post("/users/", response_model=schemas.User)
def create_user(
        user: schemas.UserCreate, db: Session = Depends(get_db_session)):

    db_user = services.get_user_by_email(db=db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=400, detail="woops the email is in use"
        )
    return services.create_user(db=db, user=user)


@references_router.get("/users/", response_model=List[schemas.User])
def read_users(
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db_session)):

    users = services.get_users(db=db, skip=skip, limit=limit)

    return users


@references_router.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db_session)):
    db_user = services.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=404, detail="sorry this user does not exists"
        )
    return db_user


@references_router.post("/vessels/", response_model=schemas.Vessel)
def create_vessel(vessel: schemas.VesselCreate, db: Session = Depends(get_db_session)):
    db_vessel = services.get_vessel_by_imo(db=db, vessel_imo=vessel.imo)
    if db_vessel:
        raise HTTPException(
            status_code=404, detail="sorry this vessel already exists"
        )

    return services.create_vessel(db=db, vessel=vessel)


"""
@app.get("/users/{user_id}/containers/", response_model=List[_schemas.Container])
def read_user_containers(
    user_id: int,
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    db_user = _services.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise _fastapi.HTTPException(
            status_code=404, detail="sorry this user does not exist"
        )

    return _services.get_containers_by_user(db=db, user=db_user)


@app.get("/containers/", response_model=List[_schemas.Container])
def read_containers(
        skip: int = 0,
        limit: int = 10,
        db: _orm.Session = _fastapi.Depends(_services.get_db)):
    containers = _services.get_containers(db=db, skip=skip, limit=limit)

    return containers


@app.get("/containers/{container_id}", response_model=_schemas.Container)
def read_containers(container_id: int, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    db_container = _services.get_container(db=db, container_id=container_id)
    if db_container is None:
        raise _fastapi.HTTPException(
            status_code=404, detail="sorry this user does not exist"
        )
    return db_container
    
"""
