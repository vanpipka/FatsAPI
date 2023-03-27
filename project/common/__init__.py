from fastapi import APIRouter

common_router = APIRouter(
    prefix="/common",
)

from . import urls, models
