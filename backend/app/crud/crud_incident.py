from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.incident import Incident
from app.schemas.incident import IncidentCreate, IncidentUpdate


class CRUDIncident(CRUDBase[Incident, IncidentCreate, IncidentUpdate]):
    def create(self, db: Session, *, obj_in: IncidentCreate) -> Incident:
        # This is a simplified create. The main logic is in the incident_service.
        db_obj = Incident(name=obj_in.name, description=obj_in.description)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


incident = CRUDIncident(Incident)
