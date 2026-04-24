import enum

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class RunbookTaskStatus(str, enum.Enum):
    NOT_STARTED = "Not Started"
    IN_PROGRESS = "In Progress"
    BLOCKED = "Blocked"
    COMPLETED = "Completed"


class RunbookTask(Base):
    __tablename__ = "runbook_tasks"

    id = Column(Integer, primary_key=True, index=True)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False)
    step_number = Column(Integer, nullable=False)
    task_description = Column(String, nullable=False)
    owner = Column(String, nullable=False)
    eta_minutes = Column(Integer, nullable=False)
    status = Column(
        SQLAlchemyEnum(RunbookTaskStatus),
        default=RunbookTaskStatus.NOT_STARTED,
        nullable=False,
    )
    evidence_required = Column(String, nullable=True)
    escalation_condition = Column(String, nullable=True)

    service = relationship("Service", back_populates="runbook_tasks")
