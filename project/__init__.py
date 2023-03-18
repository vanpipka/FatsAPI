from fastapi import FastAPI

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


    @app.get("/")
    async def root():
        return {"message": "Hello World"}

    return app
