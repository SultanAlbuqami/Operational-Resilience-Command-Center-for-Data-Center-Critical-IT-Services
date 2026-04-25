from pydantic import BaseModel


class RecoveryScoreRationale(BaseModel):
    business_impact_score: float
    time_pressure_score: float
    dependency_score: float
    urgency_ratio: float
    time_since_outage_minutes: float
    # New additions
    dependency_blockage_score: float = 0.0
    rpo_exposure_score: float = 0.0
    vendor_readiness_score: float = 0.0
    dr_site_readiness_score: float = 0.0


class RecoveryScore(BaseModel):
    service_id: int
    name: str
    total_score: float
    recovery_order: int
    rationale: RecoveryScoreRationale
