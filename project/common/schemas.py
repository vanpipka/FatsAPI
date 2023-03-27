from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class _TaskBase(BaseModel):
    id: str


class Task(_TaskBase):
    pass


class TaskFullInfo(_TaskBase):
    status: str
    name: Optional[str]
    result: Optional[str]
    date_done: Optional[datetime]


