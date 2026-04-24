from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


# A minimal service schema to avoid circular imports
class Service(BaseModel):
    id: int
    name: str
    current_status: str

    class Config:
        from_attributes = True


class IncidentBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None


class IncidentCreate(IncidentBase):
    name: str
    # The list of service names to mark as initially impacted
    initial_impacted_services: List[str] = []


class IncidentUpdate(IncidentBase):
    pass


class IncidentInDBBase(IncidentBase):
    id: int
    start_time: datetime
    end_time: Optional[datetime] = None

    class Config:
        from_attributes = True


# Properties to return to client
class Incident(IncidentInDBBase):
    affected_services: List[Service] = []


# Properties stored in DB
class IncidentInDB(IncidentInDBBase):
    pass
