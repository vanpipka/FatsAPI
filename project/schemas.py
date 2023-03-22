from datetime import datetime

from pydantic import BaseModel


class Task(BaseModel):
    id: str
    date: datetime



