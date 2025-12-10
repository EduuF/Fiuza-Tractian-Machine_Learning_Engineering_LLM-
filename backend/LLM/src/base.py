"""Base class for LLM models"""

from abc import ABC, abstractmethod


class BaseLLMStrategy(ABC):
    """
    Abstract Base Class representing the Strategy Interface for LLM generation.
    Enforces a consistent contract across different providers (OpenAI, Gemini, etc).
    """

    @abstractmethod
    def generate(self, prompt_text: str) -> str:
        """
        Generates a text completion for the given prompt.

        Args:
            prompt_text: The fully formatted prompt string.

        Returns:
            str: The generated response text.
        """
        pass
