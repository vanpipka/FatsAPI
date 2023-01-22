from typing import List

import pydantic as _pydantic


class _CategoryBase(_pydantic.BaseModel):
    name: str
    description: str
    url: str


class CategoryCreate(_CategoryBase):
    pass


class Category(_CategoryBase):
    id: int
    name: str
    description: str
    url: str


class _ArticleBase(_pydantic.BaseModel):
    title: str
    text: str


class ArticleCreate(_ArticleBase):
    pass


class Article(_ArticleBase):
    title: str
    text: str
    is_accepted: bool
    category_id: int
    user_id: int

    class Config:
        orm_mode = True


class _UserBase(_pydantic.BaseModel):
    email: str


class UserCreate(_UserBase):
    password: str


class User(_UserBase):
    id: int
    is_active: bool
    articles: List[Article]
