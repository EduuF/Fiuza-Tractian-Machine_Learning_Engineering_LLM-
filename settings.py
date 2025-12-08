"""
This module provides configuration management using Pydantic Settings,
allowing flexible loading of environment variables from different .env files.
"""

from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings configuration class.

    Loads settings from environment variables or .env files.
    """

    # V-ENV
    API_HOST: str = Field(description="Host address of the API", default="localhost")
    API_PORT: int = Field(description="Port which API will be exposed", default=8000)



@lru_cache(maxsize=1)
def get_settings(path_var: str = ".env") -> Settings:
    """
    Get application settings with caching.

    Args:
        path_var: Path to environment file (default: ".env")

    Returns:
        Settings: Configured settings instance
    """

    class DynamicSettings(Settings):
        model_config = SettingsConfigDict(env_file=path_var, case_sensitive=True)

    return DynamicSettings()  # type: ignore


SETTINGS_VAR = get_settings(".env")