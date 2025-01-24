from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

parse_settings = SettingsConfigDict(
    env_file=".env",
    env_file_encoding="utf-8",
    extra="ignore",
)


class BotConfig(BaseSettings):
    model_config = parse_settings

    bot_token: str
    owner_id: list[int]
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = Field("DEBUG")


def get_bot_config() -> BotConfig:
    return BotConfig()
