from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.DRExercise])
def read_dr_exercises(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve DR exercises.
    """
    dr_exercises = crud.dr_exercise.get_multi(db, skip=skip, limit=limit)
    return dr_exercises


@router.post("/", response_model=schemas.DRExercise)
def create_dr_exercise(
    *, db: Session = Depends(deps.get_db), dr_exercise_in: schemas.DRExerciseCreate
) -> Any:
    """
    Create new DR exercise.
    """
    dr_exercise = crud.dr_exercise.create(db=db, obj_in=dr_exercise_in)
    return dr_exercise


@router.put("/{id}", response_model=schemas.DRExercise)
def update_dr_exercise(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    dr_exercise_in: schemas.DRExerciseUpdate
) -> Any:
    """
    Update a DR exercise.
    """
    dr_exercise = crud.dr_exercise.get(db=db, id=id)
    if not dr_exercise:
        raise HTTPException(status_code=404, detail="DR Exercise not found")
    dr_exercise = crud.dr_exercise.update(
        db=db, db_obj=dr_exercise, obj_in=dr_exercise_in
    )
    return dr_exercise


@router.get("/{id}", response_model=schemas.DRExercise)
def read_dr_exercise(*, db: Session = Depends(deps.get_db), id: int) -> Any:
    """
    Get DR exercise by ID.
    """
    dr_exercise = crud.dr_exercise.get(db=db, id=id)
    if not dr_exercise:
        raise HTTPException(status_code=404, detail="DR Exercise not found")
    return dr_exercise


@router.delete("/{id}", response_model=schemas.DRExercise)
def delete_dr_exercise(*, db: Session = Depends(deps.get_db), id: int) -> Any:
    """
    Delete a DR exercise.
    """
    dr_exercise = crud.dr_exercise.get(db=db, id=id)
    if not dr_exercise:
        raise HTTPException(status_code=404, detail="DR Exercise not found")
    dr_exercise = crud.dr_exercise.remove(db=db, id=id)
    return dr_exercise
