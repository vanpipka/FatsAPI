from fastapi import Depends
from sqlalchemy.orm import Session

from project.database import get_db_session


class ReferenceMixin:

    def save(self, db: Session = Depends(get_db_session)):
        db.add(self)
        db.commit()
        db.refresh(self)
