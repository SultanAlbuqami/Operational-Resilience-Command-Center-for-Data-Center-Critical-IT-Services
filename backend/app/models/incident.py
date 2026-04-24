from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base
from app.models.service import service_incident_association


class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)

    # From the simulation scenario
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)

    start_time = Column(DateTime(timezone=True), server_default=func.now())
    end_time = Column(DateTime(timezone=True), nullable=True)
    status = Column(String, default="Active", nullable=False)

    affected_services = relationship(
        "Service", secondary=service_incident_association, back_populates="incidents"
    )
