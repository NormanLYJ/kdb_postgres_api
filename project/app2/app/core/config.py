from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI KDB+ Postgres API"
    API_VERSION: str = "1.0.0"

    # PostgreSQL settings
    DATABASE_URL: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    # KDB+ settings
    KDB_HOST: str
    KDB_PORT: int

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
