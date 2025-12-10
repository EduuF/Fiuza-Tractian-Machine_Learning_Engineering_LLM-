"""
This module contains pure functions for inserting data into a ChromaDB collection.
It acts as an abstraction layer over LangChain's add_texts method.
"""

from typing import Any, Dict, List

from langchain_chroma import Chroma


def add_chunks_to_collection(
    vector_store: Chroma, chunks: List[Dict[str, Any]]
) -> None:
    """
    Inserts a list of processed text chunks into the provided VectorStore.

    Args:
        vector_store: The LangChain Chroma instance.
        chunks: List of dictionaries containing 'id', 'text', and 'metadata'.
    """

    if not chunks:
        return

    ids = [chunk["id"] for chunk in chunks]
    texts = [chunk["text"] for chunk in chunks]
    metadatas = [chunk["metadata"] for chunk in chunks]

    vector_store.add_texts(texts=texts, metadatas=metadatas, ids=ids)
