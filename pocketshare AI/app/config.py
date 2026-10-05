from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "PocketSmart AI"

    secret_key: str = "change-this-secret-key"

    database_url: str = "sqlite:///./pocketsmart.db"

    gemini_api_key: str = ""

    # Change this in .env if your Gemini account uses another available model.
    gemini_model: str = "gemini-2.5-flash"

    gemini_timeout_seconds: int = 45

    access_token_expire_minutes: int = 120

    max_upload_mb: int = 5

    allowed_image_types: str = (
        "image/jpeg,image/png,image/webp"
    )

    cors_origins: str = (
        "http://127.0.0.1:8000,http://localhost:8000"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def cors_origin_list(self) -> list[str]:
        return [
            item.strip()
            for item in self.cors_origins.split(",")
            if item.strip()
        ]

    @property
    def allowed_image_type_list(self) -> list[str]:
        return [
            item.strip()
            for item in self.allowed_image_types.split(",")
            if item.strip()
        ]

    @property
    def max_upload_bytes(self) -> int:
        return self.max_upload_mb * 1024 * 1024


@lru_cache
def get_settings() -> Settings:
    return Settings()