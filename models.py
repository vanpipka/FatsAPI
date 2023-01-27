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

    articles = _orm.relationship("Article", back_populates="owner")
    comments = _orm.relationship("Comment", back_populates="owner")


class Category(_database.Base):

    __tablename__ = "category"

    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    name = _sql.Column(_sql.String, index=True)
    count = _sql.Column(_sql.Integer)
    description = _sql.Column(_sql.String, index=True)
    url = _sql.Column(_sql.String, index=True)


class Article(_database.Base):

    __tablename__ = "articles"

    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    title = _sql.Column(_sql.String, index=True)
    text = _sql.Column(_sql.String, index=True)
    description = _sql.Column(_sql.String, index=True)
    is_accepted = _sql.Column(_sql.Boolean, default=False)
    date = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow())
    user_id = _sql.Column(_sql.String, _sql.ForeignKey("users.id"))
    category_id = _sql.Column(_sql.String, _sql.ForeignKey("category.id"))

    category = _orm.relationship("Category", back_populates="article")
    user = _orm.relationship("User", back_populates="article")


class Comment(_database.Base):

    __tablename__ = "comments"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    text = _sql.Column(_sql.String, index=True)
    accepted = _sql.Column(_sql.Boolean, default=False)
    date = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow())
    user_id = _sql.Column(_sql.String, _sql.ForeignKey("users.id"))
    article_id = _sql.Column(_sql.String, _sql.ForeignKey("articles.id"))

    article = _orm.relationship("Article", back_populates="article")
    user = _orm.relationship("User", back_populates="user")
