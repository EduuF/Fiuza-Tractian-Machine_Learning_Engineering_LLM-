"""Instantiate a Google Gemini embedding model."""

from langchain_core.embeddings import Embeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from logs.log_generator import log_message
from settings import SETTINGS_VAR


class GeminiEmbeddingBuilder:
    """Builder responsible for instantiating Google GenAI Embeddings."""

    @staticmethod
    def create() -> Embeddings:
        """
        Creates the Google embedding model.
        """
        if not SETTINGS_VAR.GOOGLE_API_KEY:
             raise ValueError("GOOGLE_API_KEY not found in settings.")

        log_message("💻 Embeddings: Initializing Google Gemini Model...", "info")

        try:
            # O modelo text-embedding-004 é o mais atual e eficiente
            model = GoogleGenerativeAIEmbeddings(
                model=SETTINGS_VAR.GOOGLE_EMBED_MODEL,
                google_api_key=SETTINGS_VAR.GOOGLE_API_KEY
            )
            log_message("✅ Embeddings: Google Gemini model initialized successfully.", "info")
            return model
        except Exception as e:
            log_message(
                f"❌ Embeddings: Failed to initialize Google GenAI: {e}", "error"
            )
            raise e