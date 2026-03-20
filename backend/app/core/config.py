from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Application
    app_name: str = "Genesis Studio"
    debug: bool = False
    secret_key: str = "change-me-in-production"

    # Database
    database_url: str = "postgresql+asyncpg://genesis:genesis@localhost:5432/genesis_studio"

    # GitHub
    github_token: str = ""

    # LLM
    llm_provider: str = "openai"
    llm_api_key: str = ""
    llm_model: str = "gpt-4o"

    # Backend
    backend_url: str = "http://localhost:8000"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
