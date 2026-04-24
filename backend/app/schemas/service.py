from typing import List, Optional

from pydantic import BaseModel

# Import other schemas to be nested
from .bia import BIA, BIACreate
from .dependency import Dependency
from .dr_exercise import DRExercise
from .runbook import RunbookTask


# Shared properties
class ServiceBase(BaseModel):
    name: str
    owner: str
    business_unit: str
    criticality_tier: int
    primary_site: str
    dr_site: str
    vendor: Optional[str] = None
    vendor_readiness: Optional[str] = "High"
    dr_site_status: Optional[str] = "Ready"
    current_status: Optional[str] = "Operational"
    continuity_posture: Optional[str] = "Healthy"


# Properties to receive on service creation
class ServiceCreate(ServiceBase):
    bia: BIACreate


# Properties to receive on service update
class ServiceUpdate(BaseModel):
    name: Optional[str] = None
    owner: Optional[str] = None
    business_unit: Optional[str] = None
    criticality_tier: Optional[int] = None
    primary_site: Optional[str] = None
    dr_site: Optional[str] = None
    vendor: Optional[str] = None
    vendor_readiness: Optional[str] = None
    dr_site_status: Optional[str] = None
    current_status: Optional[str] = None
    continuity_posture: Optional[str] = None
    bia: Optional[BIA] = None


# Base class for properties shared by models in DB
class ServiceInDBBase(ServiceBase):
    id: int

    class Config:
        from_attributes = True


# Main schema to return to the client - a rich object with all relations
class Service(ServiceInDBBase):
    bia: Optional[BIA] = None
    downstream_dependencies: List[Dependency] = []
    upstream_dependencies: List[Dependency] = []
    runbook_tasks: List[RunbookTask] = []
    dr_exercises: List[DRExercise] = []


# Properties stored in DB
class ServiceInDB(ServiceInDBBase):
    pass


# This is a schema for a simpler list view of services
class ServiceSimple(BaseModel):
    id: int
    name: str
    criticality_tier: int
    current_status: str
    continuity_posture: str
    rto_target_hours: Optional[int] = None  # Denormalized from BIA

    class Config:
        from_attributes = True
