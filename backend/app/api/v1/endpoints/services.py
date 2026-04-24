from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Service])
def read_services(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve a list of services with their full details.
    """
    services = crud.service.get_multi(db, skip=skip, limit=limit)
    return services


@router.get("/simple", response_model=List[schemas.ServiceSimple])
def read_services_simple(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve a simplified list of services.
    """
    # This reuses the get_multi and Pydantic will handle the projection
    services = crud.service.get_multi(db, skip=skip, limit=limit)
    return services


@router.post("/", response_model=schemas.Service)
def create_service(
    *, db: Session = Depends(deps.get_db), service_in: schemas.ServiceCreate
) -> Any:
    """
    Create new service along with its Business Impact Analysis.
    """
    service = crud.service.create(db=db, obj_in=service_in)
    return service


@router.put("/{id}", response_model=schemas.Service)
def update_service(
    *, db: Session = Depends(deps.get_db), id: int, service_in: schemas.ServiceUpdate
) -> Any:
    """
    Update a service.
    """
    service = crud.service.get(db=db, id=id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    service = crud.service.update(db=db, db_obj=service, obj_in=service_in)
    return service


@router.get("/{id}", response_model=schemas.Service)
def read_service(*, db: Session = Depends(deps.get_db), id: int) -> Any:
    """
    Get service by ID with all its related data.
    """
    service = crud.service.get(db=db, id=id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return service


@router.delete("/{id}", response_model=schemas.Service)
def delete_service(*, db: Session = Depends(deps.get_db), id: int) -> Any:
    """
    Delete a service.
    """
    service = crud.service.get(db=db, id=id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    service = crud.service.remove(db=db, id=id)
    return service
