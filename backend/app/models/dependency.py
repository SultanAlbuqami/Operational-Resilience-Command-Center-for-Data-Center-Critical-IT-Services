from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Dependency(Base):
    __tablename__ = "dependencies"

    id = Column(Integer, primary_key=True, index=True)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False)
    depends_on_id = Column(Integer, ForeignKey("services.id"), nullable=True)
    dependency_name = Column(
        String, nullable=True
    )  # For external or non-service dependencies

    # The service that has the dependency
    service = relationship(
        "Service", foreign_keys=[service_id], back_populates="downstream_dependencies"
    )

    # The service that is being depended on
    depends_on = relationship(
        "Service", foreign_keys=[depends_on_id], back_populates="upstream_dependencies"
    )

    @property
    def service_name(self) -> str:
        return self.service.name

    @property
    def depends_on_name(self) -> str:
        if self.depends_on:
            return self.depends_on.name
        return self.dependency_name
