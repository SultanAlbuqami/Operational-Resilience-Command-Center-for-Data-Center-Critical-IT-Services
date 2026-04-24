from typing import List

from sqlalchemy.orm import Session, joinedload

from app.crud.base import CRUDBase
from app.models.runbook import RunbookTask
from app.schemas.runbook import RunbookTaskCreate, RunbookTaskUpdate


class CRUDRunbookTask(CRUDBase[RunbookTask, RunbookTaskCreate, RunbookTaskUpdate]):
    def get(self, db: Session, id: int) -> RunbookTask:
        return (
            db.query(self.model)
            .options(joinedload(self.model.service))
            .filter(self.model.id == id)
            .first()
        )

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[RunbookTask]:
        return (
            db.query(self.model)
            .options(joinedload(self.model.service))
            .order_by(self.model.id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_multi_by_service(
        self, db: Session, *, service_id: int, skip: int = 0, limit: int = 100
    ) -> List[RunbookTask]:
        return (
            db.query(self.model)
            .options(joinedload(self.model.service))
            .filter(RunbookTask.service_id == service_id)
            .order_by(self.model.step_number)
            .offset(skip)
            .limit(limit)
            .all()
        )


runbook_task = CRUDRunbookTask(RunbookTask)
