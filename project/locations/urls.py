import logging
import random
from string import ascii_lowercase
from typing import List

from celery.result import AsyncResult
from fastapi import Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from . import locations_router
from .models import Coordinate
from project.database import get_db_session

from . import schemas, services


@locations_router.post("/coordinates/", response_model=schemas.Coordinate)
def create_coordinate(coordinate: schemas.CoordinateCreate, db: Session = Depends(get_db_session)):

    from project.references.services import get_vessel

    db_vessel = get_vessel(db=db, vessel_id=coordinate.vessel_id)
    if not db_vessel:
        raise HTTPException(
            status_code=400, detail="vessel does not exists"
        )
    return services.create_coordinate(db=db, coordinate=coordinate)


@locations_router.post("/coordinates/download/{vessel_id}", response_model=schemas.Vessel)
def download_coordinate_for_vessel(vessel_id: int, db: Session = Depends(get_db_session)):

    from project.references.services import get_vessel
    from .tasks import download_vessel_coordinate

    db_vessel = get_vessel(db=db, vessel_id=vessel_id)
    if not db_vessel:
        raise HTTPException(
            status_code=400, detail="vessel does not exists"
        )

    download_vessel_coordinate.delay(db_vessel.marine_traffic_id)

    return db_vessel


@locations_router.get("/coordinates/{vessel_id}", response_model=List[schemas.Coordinate])
def read_coordinates_for_vessel(vessel_id: int, db: Session = Depends(get_db_session)):

    coordinates = services.get_coordinates_for_vessel(db=db, vessel_id=vessel_id)

    return coordinates

"""
@app.get("/users/{user_id}", response_model=_schemas.User)
def read_user(user_id: int, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    db_user = _services.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise _fastapi.HTTPException(
            status_code=404, detail="sorry this user does not exist"
        )
    return db_user


@app.post("/users/{user_id}/containers/", response_model=_schemas.Container)
def create_container(
    user_id: int,
    container: _schemas.ContainerCreate,
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    db_user = _services.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise _fastapi.HTTPException(
            status_code=404, detail="sorry this user does not exist"
        )

    return _services.create_container(db=db, container=container, user_id=user_id)


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
