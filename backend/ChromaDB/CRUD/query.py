"""
This module contains pure functions for querying data from a ChromaDB collection.
It handles semantic search and metadata retrieval.
"""

from typing import Any, Dict, List, cast

from langchain_chroma import Chroma
from langchain_core.documents import Document

from settings import SETTINGS_VAR


def query_collection(
    vector_store: Chroma,
    query_text: str,
    n_results: int = SETTINGS_VAR.RAG_RETRIEVAL_COUNT,
) -> List[Document]:
    """
    Queries the vector store for the most semantically similar documents.

    Args:
        vector_store: The LangChain Chroma instance.
        query_text: The user's question or search term.
        n_results: Number of top results to return.

    Returns:
        List[str]: A list of text content from the matched documents.
    """

    results = vector_store.similarity_search(query=query_text, k=n_results)

    return results


def count_documents(vector_store: Chroma) -> int:
    """Returns the total number of chunks (documents) in the collection."""
    return vector_store._collection.count()


def get_all_metadatas(vector_store: Chroma) -> List[Dict[str, Any]]:
    """
    Retrieves metadata from ALL chunks in the collection.
    Useful for reconstructing the list of uploaded files without loading heavy vectors.
    """

    data = vector_store._collection.get(include=["metadatas"])

    raw_metadatas = data.get("metadatas")

    if raw_metadatas is None:
        return []

    return cast(List[Dict[str, Any]], raw_metadatas)
