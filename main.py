from fastapi import FastAPI
import sqlalchemy.orm as _orm
import services as _services
import schemas as _schemas

app = FastAPI()
_services.create_database()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/users/", response_model=_schemas.User)
async def create_user(
        user: _schemas.UserCreate, db: _orm.Session = FastAPI.Depends(_services.get_db())):
    db_user = _services.get_user_by_email(db=db, email=user.email)
    if db_user:
        pass
        # raise FastAPI.H
