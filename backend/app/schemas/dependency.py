from typing import Optional

from pydantic import BaseModel


# Properties to receive on dependency creation
class DependencyCreate(BaseModel):
    service_id: int
    depends_on_id: Optional[int] = None
    dependency_name: Optional[str] = None


# Properties to receive on dependency update
class DependencyUpdate(BaseModel):
    pass


# Base class for properties shared by models in DB
class DependencyInDBBase(BaseModel):
    id: int
    service_id: int
    depends_on_id: Optional[int] = None
    dependency_name: Optional[str] = None

    class Config:
        from_attributes = True


# Properties to return to client (enriched)
class Dependency(DependencyInDBBase):
    service_name: Optional[str] = None
    depends_on_name: Optional[str] = None


# Properties stored in DB
class DependencyInDB(DependencyInDBBase):
    pass
