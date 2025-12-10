"""
This module contains the high-level business logic (Use Case) for the RAG.
It orchestrates the retrieval of relevant context from ChromaDB and generation via LLM.
"""

from functools import lru_cache
from typing import Any, Dict, List

from langchain_core.documents import Document

from backend.ChromaDB.chroma_manager import get_chroma_manager
from backend.LLM.llm_manager import get_llm_manager
from logs.log_generator import log_message


class AskQuestionPipeline:
    """Pipeline responsible for the Retrieval-Augmented Generation (RAG) process."""

    def __init__(self) -> None:
        """Initializes dependencies: ChromaDB (Retrieval) and LLM (Generation)."""
        self.chroma_manager = get_chroma_manager()
        self.llm_manager = get_llm_manager()

    def run(self, question: str) -> Dict[str, Any]:
        """
        Executes the RAG flow:
        1 - Retrieve relevant chunks from ChromaDB based on the question.
        2 - Generate answer using LLM with the context found.

        Args:
            question: The user's query.

        Returns:
            Dict: Contains the generated answer and the source references.
        """
        log_message(f"🔎 Pipeline: Processing question: '{question}'", "info")

        # Retrieval Phase (Semantic Search)
        relevant_docs: List[Document] = self.chroma_manager.query_similar(
            question, n_results=3
        )

        if not relevant_docs:
            log_message(
                "⚠️ Pipeline: No relevant documents found in ChromaDB.", "warning"
            )
            return {
                "answer": "I couldn't find any information regarding your question in the uploaded documents.",
                "references": [],
            }

        sources = {doc.metadata.get("source", "Unknown File") for doc in relevant_docs}
        sources_str = ", ".join(sources)

        log_message(
            f"📄 Pipeline: Found {len(relevant_docs)} relevant chunks from: [{sources_str}]",
            "info",
        )

        # Answer Generation
        generated_answer = self.llm_manager.get_answer(
            question=question, relevant_docs=relevant_docs
        )

        return {
            "answer": generated_answer,
            "references": [doc.page_content for doc in relevant_docs],
        }


@lru_cache()
def get_ask_question_pipeline() -> AskQuestionPipeline:
    return AskQuestionPipeline()
