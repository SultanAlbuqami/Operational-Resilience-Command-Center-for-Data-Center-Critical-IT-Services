from pydantic import BaseModel


class RecoveryScoreRationale(BaseModel):
    business_impact_score: float
    time_pressure_score: float
    dependency_score: float
    urgency_ratio: float
    time_since_outage_minutes: float


class RecoveryScore(BaseModel):
    service_id: int
    name: str
    total_score: float
    rationale: RecoveryScoreRationale
