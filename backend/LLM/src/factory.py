"""Coordinate the LLM model instantiation. Try OpenAI first and then Gemini as fallback."""

from backend.LLM.src.base import BaseLLMStrategy
from backend.LLM.src.models.gemini import GeminiLLMStrategy
from backend.LLM.src.models.openai import OpenAILLMStrategy
from logs.log_generator import log_message
from settings import SETTINGS_VAR


class LLMFactory:
    """
    Factory class responsible for instantiating the appropriate LLM Strategy.
    Fallback Strategy.
    """

    @staticmethod
    def create_llm() -> BaseLLMStrategy:
        """
        Orchestrates the creation of the LLM model.

        Strategy:
        1 - Attempt Primary (OpenAI).
        2 - If Primary fails (Auth/Connection), switch to Fallback (Gemini).
        """

        # 1 - First Strategy: OpenAI
        if SETTINGS_VAR.OPENAI_API_KEY:
            try:
                openai_strategy = OpenAILLMStrategy()
                log_message("🎯 LLM Factory: Using Primary Strategy (OpenAI).", "info")
                return openai_strategy
            except Exception as e:
                log_message(
                    f"⚠️ LLM Factory: Primary (OpenAI) initialization failed: {e}",
                    "warning",
                )
                log_message(
                    "🔄 LLM Factory: Switching to Fallback Strategy...", "warning"
                )
        else:
            log_message(
                "⚠️ LLM Factory: No OpenAI API Key found. Skipping to Fallback.",
                "warning",
            )

        # 2 - Fallback Strategy: Gemini
        if SETTINGS_VAR.GOOGLE_API_KEY:
            try:
                gemini_strategy = GeminiLLMStrategy()
                log_message(
                    "🛡️ LLM Factory: Using Fallback Strategy (Google Gemini).", "info"
                )
                return gemini_strategy
            except Exception as e:
                log_message(
                    f"❌ LLM Factory: Critical Fallback failure (Gemini). {e}", "error"
                )
                raise e
        else:
            log_message(
                "❌ LLM Factory: No GOOGLE_API_KEY found. Cannot initialize fallback.",
                "error",
            )
            raise ValueError("No valid LLM configuration found (OpenAI or Google).")
