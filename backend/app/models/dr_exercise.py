from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base
from app.models.service import service_dr_exercise_association


class DRExercise(Base):
    __tablename__ = "dr_exercises"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    scenario = Column(String, nullable=False)
    test_date = Column(DateTime(timezone=True), server_default=func.now())

    # Target values in minutes
    target_rto_minutes = Column(Integer, nullable=False)
    target_rpo_minutes = Column(Integer, nullable=False)

    # Actual values in minutes
    actual_rto_minutes = Column(Integer, nullable=True)
    actual_rpo_minutes = Column(Integer, nullable=True)

    passed = Column(Boolean, default=False, nullable=False)
    issues_observed = Column(String, nullable=True)
    lessons_learned = Column(String, nullable=True)
    corrective_actions = Column(String, nullable=True)
    owner = Column(String, nullable=False)
    target_closure_date = Column(DateTime(timezone=True), nullable=True)

    services = relationship(
        "Service",
        secondary=service_dr_exercise_association,
        back_populates="dr_exercises",
    )
