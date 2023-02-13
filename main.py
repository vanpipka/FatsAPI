from typing import List

import fastapi as _fastapi
import sqlalchemy.orm as _orm
import services as _services
import schemas as _schemas

app = _fastapi.FastAPI()
_services.create_database()


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.post("/users/", response_model=_schemas.User)
def create_user(
        user: _schemas.UserCreate, db: _orm.Session = _fastapi.Depends(_services.get_db)):

    db_user = _services.get_user_by_email(db=db, email=user.email)
    if db_user:
        raise _fastapi.HTTPException(
            status_code=400, detail="woops the email is in use"
        )
    return _services.create_user(db=db, user=user)


@app.get("/users/", response_model=List[_schemas.User])
def read_users(
        skip: int = 0,
        limit: int = 10,
        db: _orm.Session = _fastapi.Depends(_services.get_db)):

    users = _services.get_users(db=db, skip=skip, limit=limit)

    return users


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
