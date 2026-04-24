from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.schemas.recovery import RecoveryScore
from app.services import recovery_service

router = APIRouter()


@router.get("/prioritization/{incident_id}", response_model=List[RecoveryScore])
def get_recovery_prioritization(
    *, db: Session = Depends(deps.get_db), incident_id: int
) -> Any:
    """
    Get the recovery prioritization for a given incident.
    """
    incident = crud.incident.get(db=db, id=incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")

    if not incident.affected_services:
        return []

    scored_services = recovery_service.calculate_recovery_scores(
        services=incident.affected_services, incident_start_time=incident.start_time
    )

    return scored_services
