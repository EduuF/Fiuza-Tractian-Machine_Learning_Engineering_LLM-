"""Instaciate a Gemini LLM model."""

from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from backend.LLM.src.base import BaseLLMStrategy
from logs.log_generator import log_message
from settings import SETTINGS_VAR


class GeminiLLMStrategy(BaseLLMStrategy):
    """Implementation of the LLM Strategy using Google's Gemini API (Fallback)."""

    def __init__(self) -> None:
        """Initializes the Google Gemini Chat Model."""
        model_name = SETTINGS_VAR.GOOGLE_LLM_MODEL_NAME
        log_message(
            f"📡 LLM Strategy: Initializing Google Gemini (Model: {model_name})...",
            "info",
        )

        if not SETTINGS_VAR.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY is missing in settings.")

        self.llm = ChatGoogleGenerativeAI(
            model=model_name,
            google_api_key=SETTINGS_VAR.GOOGLE_API_KEY,
            temperature=SETTINGS_VAR.LLM_TEMPERATURE,
            convert_system_message_to_human=True,
        )

        # Test connection
        try:
            self.llm.invoke("Ping")
            log_message(
                "✅ LLM Strategy: Google Gemini connection established.", "info"
            )
        except Exception as e:
            log_message(
                f"❌ LLM Strategy: Failed to connect to Google Gemini: {e}", "error"
            )
            raise e

    def generate(self, prompt_text: str) -> str:
        """Generates a response using Google Gemini."""
        try:
            messages = [HumanMessage(content=prompt_text)]
            response = self.llm.invoke(messages)
            return str(response.content)
        except Exception as e:
            log_message(
                f"❌ LLM Strategy: Google Gemini generation failed: {e}", "error"
            )
            raise e
