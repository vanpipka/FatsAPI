from fastapi import APIRouter

references_router = APIRouter(
    prefix="/references",
)

from . import urls, models, tasks
