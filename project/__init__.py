import datetime

from fastapi import FastAPI
from celery.schedules import crontab
from project.config import settings


def create_app() -> FastAPI:
    app = FastAPI()

    from project.logging import configure_logging
    configure_logging()

    # do this before loading routes
    from project.celery_utils import create_celery
    app.celery_app = create_celery()

    from project.references import references_router
    app.include_router(references_router)

    from project.locations import locations_router
    app.include_router(locations_router)

    @app.get("/")
    async def root():
        return {"message": "Hello World"}

    @app.celery_app.task
    def test():
        return datetime.datetime.now()

    return app

