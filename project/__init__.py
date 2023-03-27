import datetime

from fastapi import FastAPI
from celery.schedules import crontab
from starlette.middleware.cors import CORSMiddleware

from project.config import settings


def create_app() -> FastAPI:

    app = FastAPI()

    origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    from project.logging import configure_logging
    configure_logging()

    # do this before loading routes
    from project.celery_utils import create_celery
    app.celery_app = create_celery()

    from project.references import references_router
    app.include_router(references_router)

    from project.locations import locations_router
    app.include_router(locations_router)

    from project.common import common_router
    app.include_router(common_router)

    @app.get("/")
    async def root():
        return {"message": "Hello World"}

    return app

