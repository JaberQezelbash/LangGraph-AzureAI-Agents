from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    environment: str = "local"
    azure_openai_endpoint: str | None = None
    azure_openai_api_key: str | None = None
    azure_openai_deployment: str | None = None
    azure_openai_api_version: str = "2024-12-01-preview"
    azure_content_safety_endpoint: str | None = None
    azure_content_safety_key: str | None = None
    use_azure_openai_triage: bool = False
    use_azure_openai_response: bool = False
    use_azure_content_safety: bool = False


@lru_cache
def get_settings() -> Settings:
    return Settings()
