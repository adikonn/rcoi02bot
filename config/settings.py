from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional


class Settings(BaseSettings):
    bot_token: str = Field('', env="BOT_TOKEN")
    database_url: str = Field("sqlite+aiosqlite:///bot.db", env="DATABASE_URL")
    log_level: str = Field("INFO", env="LOG_LEVEL")
    check_interval: int = Field(600, env="CHECK_INTERVAL")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
