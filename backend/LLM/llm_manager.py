"""The main interface for ChromaDB opertations"""

from functools import lru_cache
from typing import List

from langchain_core.documents import Document

from backend.LLM.prompts.prompt_loader import load_prompt_from_yaml
from backend.LLM.src.base import BaseLLMStrategy
from backend.LLM.src.factory import LLMFactory
from logs.log_generator import log_message


class LLMManager:
    """
    Facade class that simplifies interaction with the LLM subsystem.
    It handles Strategy selection (via Factory) and Prompt formatting.
    """

    def __init__(self) -> None:
        """Initializes the LLM Strategy and loads the Prompt Template."""
        self.llm: BaseLLMStrategy = LLMFactory.create_llm()

        self.prompt_template = load_prompt_from_yaml("rag_prompt.yaml")

    def get_answer(self, question: str, relevant_docs: List[Document]) -> str:
        """
        Composes the context and question into a prompt and gets the answer from the LLM.

        Args:
            question: The user's query.
            relevant_chunks: List of text strings retrieved from ChromaDB.

        Returns:
            str: The generated answer.
        """
        # Prepare Context (Extract page_content from Documents)
        context_text = "\n\n".join([doc.page_content for doc in relevant_docs])

        # Format Prompt
        formatted_prompt = self.prompt_template.format(
            context=context_text, question=question
        )

        log_message(
            "🤖 LLM Manager: Sending formatted prompt to LLM for generation...", "info"
        )

        # Generate
        try:
            response = self.llm.generate(formatted_prompt)
            return response
        except Exception as e:
            log_message(f"❌ LLM Manager: Error during generation: {e}", "error")
            return "I apologize, but an internal error occurred while generating the answer."


@lru_cache()
def get_llm_manager() -> LLMManager:
    """Singleton accessor for LLMManager."""
    return LLMManager()
