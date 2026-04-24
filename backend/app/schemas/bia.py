from typing import Optional

from pydantic import BaseModel


# Shared properties
class BIABase(BaseModel):
    rto_target_hours: Optional[float] = None
    rpo_target_minutes: Optional[int] = None
    financial_impact: Optional[str] = None
    regulatory_impact: Optional[str] = None
    reputational_impact: Optional[str] = None
    key_business_process_supported: Optional[str] = None


# Properties to receive on BIA creation
class BIACreate(BIABase):
    rto_target_hours: float
    rpo_target_minutes: int
    financial_impact: str
    regulatory_impact: str
    reputational_impact: str
    key_business_process_supported: str


# Properties to receive on BIA update
class BIAUpdate(BIABase):
    pass


# Properties shared by models in DB
class BIAInDBBase(BIABase):
    id: int
    service_id: int

    class Config:
        from_attributes = True


# Properties to return to client
class BIA(BIAInDBBase):
    pass


# Properties stored in DB
class BIAInDB(BIAInDBBase):
    pass
