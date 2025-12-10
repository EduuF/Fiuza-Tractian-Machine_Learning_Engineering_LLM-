from functools import lru_cache
from pathlib import Path

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

# Resolve the project root directory dynamically
BASE_DIR = Path(__file__).resolve().parent


class Settings(BaseSettings):
    """
    Application configuration settings.
    Values are read from .env file or environment variables.
    """

    # --- Authentication Keys ---
    OPENAI_API_KEY: SecretStr = Field(
        default=SecretStr(""), description="OpenAI API Key"
    )
    GOOGLE_API_KEY: SecretStr = Field(
        default=SecretStr(""), description="Google Gemini API Key"
    )

    # --- API Configuration ---
    API_HOST: str = Field(default="0.0.0.0", description="Host to bind the server")
    API_PORT: int = Field(default=8000, description="Port to bind the server")

    # --- Storage Configuration ---
    # Relative path from project root
    CHROMA_DB_PATH: str = Field(
        default="./backend/ChromaDB/DB_instance",
        description="Path for Vector DB persistence",
    )

    # --- Embedding Models ---
    OPENAI_EMBED_MODEL_NAME: str = Field(default="text-embedding-3-small")
    GOOGLE_EMBED_MODEL: str = Field(default="models/text-embedding-004")

    # --- LLM Generation Models ---
    OPENAI_LLM_MODEL_NAME: str = Field(
        default="gpt-3.5-turbo", description="Primary LLM Model"
    )
    GOOGLE_LLM_MODEL_NAME: str = Field(
        default="gemini-pro", description="Fallback Gemini Model"
    )

    # --- RAG Tuning ---
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    LLM_TEMPERATURE: float = 0.5
    RAG_RETRIEVAL_COUNT: int = Field(
        default=3, description="Top-K chunks to retrieve for RAG"
    )

    @property
    def database_path(self) -> str:
        """Returns the absolute OS path for the database, ensuring portability."""
        absolute_path = BASE_DIR / self.CHROMA_DB_PATH
        return str(absolute_path.resolve())


@lru_cache(maxsize=1)
def get_settings(path_var: str = ".env") -> Settings:
    """Singleton factory for Settings."""
    class DynamicSettings(Settings):
        model_config = SettingsConfigDict(
            env_file=path_var,
            case_sensitive=True,
            extra="ignore",
            env_file_encoding="utf-8",
        )

    return DynamicSettings()


SETTINGS_VAR = get_settings(".env")
