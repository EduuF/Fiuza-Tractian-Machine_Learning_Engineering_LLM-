"""Instanciate an OpenAI Embeddings model."""

from langchain_core.embeddings import Embeddings
from langchain_openai import OpenAIEmbeddings

from logs.log_generator import log_message
from settings import SETTINGS_VAR


class OpenAIEmbeddingBuilder:
    """Builder responsible for instantiating and validating OpenAI Embeddings."""

    @staticmethod
    def create() -> Embeddings:
        """Creates the OpenAI Embeddings model."""
        if not SETTINGS_VAR.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not found in settings.")

        log_message("📡 Embeddings: Attempting to initialize OpenAI...", "info")

        model = OpenAIEmbeddings(
            model=SETTINGS_VAR.OPENAI_EMBED_MODEL_NAME,
            api_key=SETTINGS_VAR.OPENAI_API_KEY,
        )

        # Test the connection
        model.embed_query("test")

        log_message("✅ Embeddings: OpenAI initialized and validated.", "info")
        return model
