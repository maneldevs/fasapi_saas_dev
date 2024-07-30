from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "FASTAPI"
    app_version: str = "0.0.1"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
