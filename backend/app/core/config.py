from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Operational Resilience Command Center"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = "sqlite:///./resilience_command_center.db"

    class Config:
        case_sensitive = True


settings = Settings()
