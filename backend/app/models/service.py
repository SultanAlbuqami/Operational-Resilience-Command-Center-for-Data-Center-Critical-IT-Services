from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from app.db.base_class import Base

# Association Table for Service and DRExercise
service_dr_exercise_association = Table(
    "service_dr_exercise_association",
    Base.metadata,
    Column("service_id", Integer, ForeignKey("services.id"), primary_key=True),
    Column("dr_exercise_id", Integer, ForeignKey("dr_exercises.id"), primary_key=True),
)

# Association Table for Service and Incident
service_incident_association = Table(
    "service_incident_association",
    Base.metadata,
    Column("service_id", Integer, ForeignKey("services.id"), primary_key=True),
    Column("incident_id", Integer, ForeignKey("incidents.id"), primary_key=True),
)


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False, unique=True)
    owner = Column(String, nullable=False)
    business_unit = Column(String, nullable=False)

    # From BIA, denormalized for easier access
    criticality_tier = Column(Integer, nullable=False)

    primary_site = Column(String, nullable=False)
    dr_site = Column(String, nullable=False)

    current_status = Column(String, default="Operational", nullable=False)
    continuity_posture = Column(String, default="Healthy", nullable=False)

    bia = relationship(
        "BIA", back_populates="service", uselist=False, cascade="all, delete-orphan"
    )

    # Dependencies where this service is the source (e.g. "CRM" depends on "Identity")
    downstream_dependencies = relationship(
        "Dependency",
        foreign_keys="[Dependency.service_id]",
        back_populates="service",
        cascade="all, delete-orphan",
    )

    # Dependencies where this service is the target
    # (e.g. "CRM" is a dependency for "Billing")
    upstream_dependencies = relationship(
        "Dependency",
        foreign_keys="[Dependency.depends_on_id]",
        back_populates="depends_on",
    )

    runbook_tasks = relationship(
        "RunbookTask", back_populates="service", cascade="all, delete-orphan"
    )

    dr_exercises = relationship(
        "DRExercise",
        secondary=service_dr_exercise_association,
        back_populates="services",
    )

    incidents = relationship(
        "Incident",
        secondary=service_incident_association,
        back_populates="affected_services",
    )
