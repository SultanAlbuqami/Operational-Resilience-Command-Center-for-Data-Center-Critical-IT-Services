from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.dr_exercise import DRExercise
from app.models.service import Service
from app.schemas.dr_exercise import DRExerciseCreate, DRExerciseUpdate


class CRUDDRExercise(CRUDBase[DRExercise, DRExerciseCreate, DRExerciseUpdate]):
    def create(self, db: Session, *, obj_in: DRExerciseCreate) -> DRExercise:
        db_obj = DRExercise(
            name=obj_in.name,
            scenario=obj_in.scenario,
            target_rto_minutes=obj_in.target_rto_minutes,
            target_rpo_minutes=obj_in.target_rpo_minutes,
            owner=obj_in.owner,
        )
        if obj_in.service_ids:
            services = (
                db.query(Service).filter(Service.id.in_(obj_in.service_ids)).all()
            )
            db_obj.services.extend(services)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: DRExercise, obj_in: DRExerciseUpdate
    ) -> DRExercise:
        # Update scalar fields
        update_data = obj_in.dict(exclude_unset=True)
        if "service_ids" in update_data:
            del update_data["service_ids"]

        for field, value in update_data.items():
            setattr(db_obj, field, value)

        # Update many-to-many relationship
        if obj_in.service_ids is not None:
            services = (
                db.query(Service).filter(Service.id.in_(obj_in.service_ids)).all()
            )
            db_obj.services = services

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


dr_exercise = CRUDDRExercise(DRExercise)
