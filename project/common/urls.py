from datetime import datetime
from typing import List

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from . import common_router
from project.database import get_db_session

from . import schemas, services


@common_router.get("/task/{task_id}", response_model=schemas.TaskFullInfo)
def read_task(task_id: str, db: Session = Depends(get_db_session)):

    from celery.result import AsyncResult
    task = AsyncResult(task_id)

    return {"id": task.id,
            "name": task.name,
            "status": task.status,
            "date_done": task.date_done,
            "result": str(task.result)}


