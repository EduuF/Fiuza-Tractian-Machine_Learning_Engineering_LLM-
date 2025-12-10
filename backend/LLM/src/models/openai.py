"""Instaciate a OpenAI LLM model."""

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

from backend.LLM.src.base import BaseLLMStrategy
from logs.log_generator import log_message
from settings import SETTINGS_VAR


class OpenAILLMStrategy(BaseLLMStrategy):
    """Implementation of the LLM Strategy using OpenAI's API."""

    def __init__(self) -> None:
        """
        Initializes the OpenAI Chat Model.
        Performs a connection check upon instantiation.
        """
        model_name = SETTINGS_VAR.OPENAI_LLM_MODEL_NAME
        log_message(
            f"📡 LLM Strategy: Initializing OpenAI (Model: {model_name})...", "info"
        )

        self.llm = ChatOpenAI(
            api_key=SETTINGS_VAR.OPENAI_API_KEY,
            model=model_name,
            temperature=SETTINGS_VAR.LLM_TEMPERATURE,
        )

        # Test connection
        try:
            self.llm.invoke([HumanMessage(content="ping")])
            log_message("✅ LLM Strategy: OpenAI connection established.", "info")
        except Exception as e:
            raise e

    def generate(self, prompt_text: str) -> str:
        """Generates a response using OpenAI."""
        try:
            messages = [HumanMessage(content=prompt_text)]
            response = self.llm.invoke(messages)
            return str(response.content)
        except Exception as e:
            log_message(f"❌ LLM Strategy: OpenAI generation failed: {e}", "error")
            raise e
