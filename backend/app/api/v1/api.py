from fastapi import APIRouter

from app.api.v1.endpoints import (
    dependencies,
    dr_exercises,
    incidents,
    recovery,
    runbooks,
    services,
)

api_router = APIRouter()
api_router.include_router(services.router, prefix="/services", tags=["Services"])
api_router.include_router(
    dependencies.router, prefix="/dependencies", tags=["Dependencies"]
)
api_router.include_router(incidents.router, prefix="/incidents", tags=["Incidents"])
api_router.include_router(runbooks.router, prefix="/runbooks", tags=["Runbooks"])
api_router.include_router(
    dr_exercises.router, prefix="/dr-exercises", tags=["DR Exercises"]
)
api_router.include_router(recovery.router, prefix="/recovery", tags=["Recovery"])
