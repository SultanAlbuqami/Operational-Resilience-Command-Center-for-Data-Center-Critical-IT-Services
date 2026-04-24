from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Dependency])
def read_dependencies(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve dependencies.
    """
    dependencies = crud.dependency.get_multi(db, skip=skip, limit=limit)
    return dependencies


@router.post("/", response_model=schemas.Dependency)
def create_dependency(
    *, db: Session = Depends(deps.get_db), dependency_in: schemas.DependencyCreate
) -> Any:
    """
    Create new dependency.
    """
    dependency = crud.dependency.create(db=db, obj_in=dependency_in)
    return dependency


@router.get("/{id}", response_model=schemas.Dependency)
def read_dependency(*, db: Session = Depends(deps.get_db), id: int) -> Any:
    """
    Get dependency by ID.
    """
    dependency = crud.dependency.get(db=db, id=id)
    if not dependency:
        raise HTTPException(status_code=404, detail="Dependency not found")
    return dependency


@router.delete("/{id}", response_model=schemas.Dependency)
def delete_dependency(*, db: Session = Depends(deps.get_db), id: int) -> Any:
    """
    Delete a dependency.
    """
    dependency = crud.dependency.get(db=db, id=id)
    if not dependency:
        raise HTTPException(status_code=404, detail="Dependency not found")
    dependency = crud.dependency.remove(db=db, id=id)
    return dependency
