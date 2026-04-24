from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


# A minimal service schema to avoid circular imports
class Service(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class DRExerciseBase(BaseModel):
    name: Optional[str] = None
    scenario: Optional[str] = None
    target_rto_minutes: Optional[int] = None
    target_rpo_minutes: Optional[int] = None
    actual_rto_minutes: Optional[int] = None
    actual_rpo_minutes: Optional[int] = None
    passed: Optional[bool] = None
    issues_observed: Optional[str] = None
    lessons_learned: Optional[str] = None
    corrective_actions: Optional[str] = None
    owner: Optional[str] = None
    target_closure_date: Optional[datetime] = None


class DRExerciseCreate(DRExerciseBase):
    name: str
    scenario: str
    target_rto_minutes: int
    target_rpo_minutes: int
    owner: str
    service_ids: List[int] = []


class DRExerciseUpdate(DRExerciseBase):
    service_ids: Optional[List[int]] = None


class DRExerciseInDBBase(DRExerciseBase):
    id: int
    test_date: datetime

    class Config:
        from_attributes = True


# Properties to return to client
class DRExercise(DRExerciseInDBBase):
    services: List[Service] = []


class DRExerciseInDB(DRExerciseInDBBase):
    pass
