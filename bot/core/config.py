"""Bot configuration.

Bot = UI only layer. All data and logic via backend HTTP API.
"""
from pydantic_settings import BaseSettings


class BotSettings(BaseSettings):
    telegram_bot_token: str = ""
    backend_url: str = "http://localhost:8000"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


bot_settings = BotSettings()
