from fastapi import FastAPI

from app.api.v1.api import api_router
from app.core.config import settings
from app.db.base import Base
from app.db.database import engine


def create_tables():
    Base.metadata.create_all(bind=engine)


app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)


@app.on_event("startup")
def on_startup():
    create_tables()


app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/", tags=["Root"])
def read_root():
    return {"message": f"Welcome to the {settings.PROJECT_NAME} API"}
