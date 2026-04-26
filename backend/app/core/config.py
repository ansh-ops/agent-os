from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Agent OS"
    api_prefix: str = "/api"
    cors_origins: list[str] = ["http://localhost:3000"]
    data_dir: Path = Path("data")
    tasks_dir_name: str = "tasks"
    uploads_dir_name: str = "uploads"
    llm_provider: str = "gemini"
    use_mock_agents: bool = True
    gemini_api_key: str | None = None
    openai_api_key: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def tasks_dir(self) -> Path:
        return self.data_dir / self.tasks_dir_name

    @property
    def uploads_dir(self) -> Path:
        return self.data_dir / self.uploads_dir_name


settings = Settings()
