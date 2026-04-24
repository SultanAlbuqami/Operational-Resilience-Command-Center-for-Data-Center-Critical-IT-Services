from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.RunbookTask])
def read_runbook_tasks(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    service_id: Optional[int] = None,
) -> Any:
    """
    Retrieve runbook tasks, optionally filtered by service.
    """
    if service_id is not None:
        runbook_tasks = crud.runbook_task.get_multi_by_service(
            db, service_id=service_id, skip=skip, limit=limit
        )
    else:
        runbook_tasks = crud.runbook_task.get_multi(db, skip=skip, limit=limit)
    return runbook_tasks


@router.post("/", response_model=schemas.RunbookTask)
def create_runbook_task(
    *, db: Session = Depends(deps.get_db), runbook_task_in: schemas.RunbookTaskCreate
) -> Any:
    """
    Create new runbook task.
    """
    runbook_task = crud.runbook_task.create(db=db, obj_in=runbook_task_in)
    return runbook_task


@router.put("/{id}", response_model=schemas.RunbookTask)
def update_runbook_task(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    runbook_task_in: schemas.RunbookTaskUpdate
) -> Any:
    """
    Update a runbook task.
    """
    runbook_task = crud.runbook_task.get(db=db, id=id)
    if not runbook_task:
        raise HTTPException(status_code=404, detail="Runbook task not found")
    runbook_task = crud.runbook_task.update(
        db=db, db_obj=runbook_task, obj_in=runbook_task_in
    )
    return runbook_task


@router.get("/{id}", response_model=schemas.RunbookTask)
def read_runbook_task(*, db: Session = Depends(deps.get_db), id: int) -> Any:
    """
    Get runbook task by ID.
    """
    runbook_task = crud.runbook_task.get(db=db, id=id)
    if not runbook_task:
        raise HTTPException(status_code=404, detail="Runbook task not found")
    return runbook_task


@router.delete("/{id}", response_model=schemas.RunbookTask)
def delete_runbook_task(*, db: Session = Depends(deps.get_db), id: int) -> Any:
    """
    Delete a runbook task.
    """
    runbook_task = crud.runbook_task.get(db=db, id=id)
    if not runbook_task:
        raise HTTPException(status_code=404, detail="Runbook task not found")
    runbook_task = crud.runbook_task.remove(db=db, id=id)
    return runbook_task
