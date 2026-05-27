import os
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):

    openai_api_key: str = Field(validation_alias="OPENAI_API_KEY", default="")
    openai_base_url: str = Field(default="https://api.openai.com/v1", validation_alias="OPENAI_BASE_URL")
    llm_model: str = Field(default="gpt-5.5-2026-04-23", validation_alias="LLM_MODEL")
    embedding_model: str = Field(default="text-embedding-3-large", validation_alias="EMBEDDING_MODEL")

    database_url: str = Field(validation_alias="DATABASE_URL")

    max_chunks_returned: int = Field(default=6, validation_alias="MAX_CHUNKS_RETURNED")
    cache_ttl_seconds: int = Field(default=600, validation_alias="CACHE_TTL_SECONDS")
    max_file_size_mb: int = Field(default=50, validation_alias="MAX_FILE_SIZE_MB")

    cors_origins: str = Field(default="http://localhost:5173", validation_alias="CORS_ORIGINS")

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",")]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False
    )

@lru_cache()
def get_settings() -> Settings:
    return Settings()
