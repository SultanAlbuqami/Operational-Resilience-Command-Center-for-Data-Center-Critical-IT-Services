from typing import Optional

from pydantic import BaseModel

from app.models.runbook import RunbookTaskStatus


# A minimal service schema to avoid circular imports
class ServiceSimple(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


# Shared properties
class RunbookTaskBase(BaseModel):
    step_number: Optional[int] = None
    task_description: Optional[str] = None
    owner: Optional[str] = None
    eta_minutes: Optional[int] = None
    status: Optional[RunbookTaskStatus] = None
    evidence_required: Optional[str] = None
    escalation_condition: Optional[str] = None


# Properties to receive on task creation
class RunbookTaskCreate(RunbookTaskBase):
    service_id: int
    step_number: int
    task_description: str
    owner: str
    eta_minutes: int


# Properties to receive on task update
class RunbookTaskUpdate(RunbookTaskBase):
    pass


# Properties shared by models in DB
class RunbookTaskInDBBase(RunbookTaskBase):
    id: int
    service_id: int

    class Config:
        from_attributes = True


# Properties to return to client
class RunbookTask(RunbookTaskInDBBase):
    service: Optional[ServiceSimple] = None


# Properties stored in DB
class RunbookTaskInDB(RunbookTaskInDBBase):
    pass
