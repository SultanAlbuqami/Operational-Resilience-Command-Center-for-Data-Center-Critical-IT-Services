from app.crud.base import CRUDBase
from app.models.dependency import Dependency
from app.schemas.dependency import DependencyCreate, DependencyUpdate


class CRUDDependency(CRUDBase[Dependency, DependencyCreate, DependencyUpdate]):
    pass


dependency = CRUDDependency(Dependency)
