from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps
from app.services import incident_service

router = APIRouter()


@router.get("/", response_model=List[schemas.Incident])
def read_incidents(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve incidents.
    """
    incidents = crud.incident.get_multi(db, skip=skip, limit=limit)
    return incidents


@router.post("/trigger", response_model=schemas.Incident)
def trigger_new_incident(
    *, db: Session = Depends(deps.get_db), incident_in: schemas.IncidentCreate
) -> Any:
    """
    Trigger a new incident simulation.
    """
    incident = incident_service.trigger_incident(
        db, scenario_name=incident_in.name, description=incident_in.description
    )
    if not incident:
        raise HTTPException(
            status_code=404,
            detail=f"Scenario '{incident_in.name}' not found or has no impact.",
        )
    return incident


@router.get("/{id}", response_model=schemas.Incident)
def read_incident(*, db: Session = Depends(deps.get_db), id: int) -> Any:
    """
    Get incident by ID.
    """
    incident = crud.incident.get(db=db, id=id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident


@router.get("/{id}/executive-brief", response_model=schemas.ExecutiveBrief)
def get_executive_brief(*, db: Session = Depends(deps.get_db), id: int) -> Any:
    """
    Get an executive brief for a specific incident.
    """
    incident = crud.incident.get(db=db, id=id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")

    return incident_service.generate_executive_brief(incident)
