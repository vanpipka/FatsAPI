from typing import List

from fastapi import Depends, HTTPException
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


@references_router.get("/vessels/", response_model=List[schemas.Vessel])
def read_vessels(
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db_session)):
    vessels = services.get_vessels(db=db, skip=skip, limit=limit)

    return vessels


@references_router.get("/vessels/list/", response_model=List[schemas.VesselList])
def read_vessels(
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db_session)):
    vessels = services.get_vessels_list(db=db, skip=skip, limit=limit)

    return vessels


@references_router.get("/vessels/{vessel_id}", response_model=schemas.Vessel)
def read_vessel(vessel_id: int, db: Session = Depends(get_db_session)):
    db_vessel = services.get_vessel(db=db, vessel_id=vessel_id)
    if db_vessel is None:
        raise HTTPException(
            status_code=404, detail="sorry this vessel does not exists"
        )
    return db_vessel


@references_router.get("/vessels/refresh_vessel_info/{vessel_id}", response_model=schemas.Vessel)
def refresh_vessel_info(vessel_id: int, db: Session = Depends(get_db_session)):

    from .tasks import refresh_vessel_info_from_marine_traffic
    db_vessel = services.get_vessel(db=db, vessel_id=vessel_id)
    if db_vessel is None:
        raise HTTPException(
            status_code=404, detail="sorry this vessel does not exists"
        )

    refresh_vessel_info_from_marine_traffic.delay(db_vessel.marine_traffic_id)

    return db_vessel


@references_router.post("/containers/", response_model=schemas.Container)
def create_container(
        container: schemas.ContainerCreate, db: Session = Depends(get_db_session)):

    db_container = services.get_container_by_name(db=db, name=container.name)
    if db_container:
        raise HTTPException(
            status_code=400, detail="woops the already used"
        )
    return services.create_container(db=db, container=container)


@references_router.get("/containers/", response_model=List[schemas.Container])
def read_containers(
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db_session)):

    containers = services.get_containers(db=db, skip=skip, limit=limit)

    return containers


@references_router.get("/containers/{container_id}", response_model=schemas.Container)
def read_container(container_id: int, db: Session = Depends(get_db_session)):
    db_container = services.get_container(db=db, container_id=container_id)
    if db_container is None:
        raise HTTPException(
            status_code=404, detail="sorry this container does not exists"
        )
    return db_container
