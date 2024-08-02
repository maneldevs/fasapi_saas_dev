from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "FASTAPI"
    app_version: str = "0.0.1"
    db_username: str
    db_password: str
    db_hostname: str
    db_port: str
    db_database: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
