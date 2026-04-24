from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class BIA(Base):
    __tablename__ = "bia"

    id = Column(Integer, primary_key=True, index=True)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False, unique=True)

    rto_target_hours = Column(Integer, nullable=False)
    rpo_target_minutes = Column(Integer, nullable=False)

    financial_impact = Column(String, nullable=False)
    regulatory_impact = Column(String, nullable=False)
    reputational_impact = Column(String, nullable=False)

    key_business_process_supported = Column(String, nullable=False)

    service = relationship("Service", back_populates="bia")
