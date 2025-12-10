"""Coordinate the embedding model instantiation. Try OpenAI first and than HF as fallback."""

from langchain_core.embeddings import Embeddings

from backend.ChromaDB.src.embeddings.models.gemini import GeminiEmbeddingBuilder
from backend.ChromaDB.src.embeddings.models.openai import OpenAIEmbeddingBuilder
from logs.log_generator import log_message
from settings import SETTINGS_VAR


class EmbeddingFactory:
    """
    Factory class to coordinate the creation of the Embedding Model.
    Fallback Strategy.
    """

    @staticmethod
    def create_embedding_model() -> Embeddings:
        """
        Orchestrates the creation of the embedding model.

        Strategy:
        1 - Attempt Primary (OpenAI).
        2 - If Primary fails (Auth/Connection), switch to Fallback (HuggingFace).
        """

        # 1 - First Strategy: OpenAI
        if SETTINGS_VAR.OPENAI_API_KEY:
            try:
                return OpenAIEmbeddingBuilder.create()
            except Exception as e:
                log_message(f"⚠️ Embeddings: Primary (OpenAI) failed: {e}", "warning")
                log_message(
                    "🔄 Embeddings: Switching to Fallback Strategy...", "warning"
                )
        else:
            log_message(
                "⚠️ Embeddings: No OpenAI API Key found. Skipping to Fallback.",
                "warning",
            )

        # 2 - Fallback Strategy: Google Gemini
        try:
            return GeminiEmbeddingBuilder.create()
        except Exception as e:
            log_message(f"❌ Embeddings: Critical Fallback failure. {e}", "error")
            raise e
