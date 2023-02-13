import sqlalchemy as _sql
import sqlalchemy.orm as _orm
import datetime as _dt

import database as _database


class User(_database.Base):

    __tablename__ = "users"

    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    email = _sql.Column(_sql.String, unique=True, index=True)
    phone = _sql.Column(_sql.String, index=True)
    hashed_password = _sql.Column(_sql.String)
    is_active = _sql.Column(_sql.Boolean, default=True)

    containers = _orm.relationship("Container", back_populates="user")


class Container(_database.Base):

    __tablename__ = "container"

    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    name = _sql.Column(_sql.String, index=True)
    user_id = _sql.Column(_sql.Integer, _sql.ForeignKey("users.id"))

    coordinates = _orm.relationship("Coordinate", back_populates="container")
    user = _orm.relationship("User", back_populates="containers")


class Coordinate(_database.Base):

    __tablename__ = "coordinate"

    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    name = _sql.Column(_sql.String, index=True)
    description = _sql.Column(_sql.String, index=True)
    url = _sql.Column(_sql.String, index=True)
    date = _sql.Column(_sql.DateTime, index=True)
    latitude = _sql.Column(_sql.String)
    longitude = _sql.Column(_sql.String)
    container_id = _sql.Column(_sql.Integer, _sql.ForeignKey("container.id"))

    container = _orm.relationship("Container", back_populates="coordinates")
