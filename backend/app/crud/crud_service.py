from typing import List

from sqlalchemy.orm import Session, joinedload

from app.crud.base import CRUDBase
from app.models.bia import BIA
from app.models.dependency import Dependency
from app.models.service import Service
from app.schemas.service import ServiceCreate, ServiceUpdate


class CRUDService(CRUDBase[Service, ServiceCreate, ServiceUpdate]):
    def create(self, db: Session, *, obj_in: ServiceCreate) -> Service:
        # Create the Service instance
        db_obj = Service(
            name=obj_in.name,
            owner=obj_in.owner,
            business_unit=obj_in.business_unit,
            criticality_tier=obj_in.criticality_tier,
            primary_site=obj_in.primary_site,
            dr_site=obj_in.dr_site,
            current_status=obj_in.current_status,
            continuity_posture=obj_in.continuity_posture,
        )

        # Create the BIA instance and associate it
        bia_data = obj_in.bia
        db_bia = BIA(**bia_data.dict())
        db_obj.bia = db_bia

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Service]:
        return (
            db.query(self.model)
            .options(joinedload(Service.bia))
            .order_by(self.model.id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get(self, db: Session, id: int) -> Service:
        return (
            db.query(self.model)
            .options(
                joinedload(Service.bia),
                joinedload(Service.downstream_dependencies).joinedload(
                    Dependency.depends_on
                ),
                joinedload(Service.upstream_dependencies).joinedload(
                    Dependency.service
                ),
                joinedload(Service.runbook_tasks),
                joinedload(Service.dr_exercises),
            )
            .filter(self.model.id == id)
            .first()
        )


service = CRUDService(Service)
