from fastapi import APIRouter

locations_router = APIRouter(
    prefix="/locations",
)

from . import urls, models, tasks
