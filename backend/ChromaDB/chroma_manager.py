"""The main interface for ChromaDB opertations"""

from functools import lru_cache
from typing import Any, Dict, List

import chromadb
from langchain_chroma import Chroma
from langchain_core.documents import Document

from backend.ChromaDB.CRUD.delete import delete_documents_by_metadata, reset_collection

# CRUD Operations
from backend.ChromaDB.CRUD.insert import add_chunks_to_collection
from backend.ChromaDB.CRUD.query import (
    count_documents,
    get_all_metadatas,
    query_collection,
)
from backend.ChromaDB.src.embeddings.factory import EmbeddingFactory
from logs.log_generator import log_message
from settings import SETTINGS_VAR


class ChromaManager:
    """
    Singleton class that manages the ChromaDB connection and operations.
    It acts as a Facade for the CRUD module and handles Embedding strategies.
    """

    def __init__(self) -> None:
        """Initializes the ChromaDB VectorStore with an explicit PersistentClient."""
        self.collection_name = "documents"
        self.persist_path = SETTINGS_VAR.database_path

        log_message(
            f"📁 ChromaDB: Connecting to persistent storage at: {self.persist_path}",
            "info",
        )

        # Load Embedding Model via Factory
        self.embedding_fn = EmbeddingFactory.create_embedding_model()

        # Initialize Native Client explicitly
        self.client = chromadb.PersistentClient(path=self.persist_path)

        # Initialize LangChain Wrapper
        self.vector_store = Chroma(
            client=self.client,
            collection_name=self.collection_name,
            embedding_function=self.embedding_fn,
        )

        # Perform Safety Checks
        self._ensure_dimension_compatibility()

    def _ensure_dimension_compatibility(self) -> None:
        """
        Validates if existing DB dimensions match the current embedding model.
        Protects against vector dimension mismatch errors during fallback switching.
        """
        collection_count = self.vector_store._collection.count()
        if collection_count == 0:
            return

        existing_data = self.vector_store._collection.get(
            limit=1, include=["embeddings"]
        )
        embeddings = existing_data.get("embeddings")

        if embeddings is None or len(embeddings) == 0:
            return

        existing_dim = len(embeddings[0])

        # Calculate current model dimension
        test_embed = self.embedding_fn.embed_query("test")
        current_dim = len(test_embed)

        if existing_dim != current_dim:
            log_message(
                f"⚠️ ChromaDB: Dimension Mismatch! DB={existing_dim}, Model={current_dim}. Resetting collection.",
                "warning",
            )
            self.reset()
        else:
            log_message("✅ ChromaDB: Dimension check passed.", "info")

    def add_chunks(self, chunks: List[Dict[str, Any]]) -> None:
        """Delegates chunk addition to CRUD module."""
        add_chunks_to_collection(self.vector_store, chunks)

    def query_similar(
        self, query_text: str, n_results: int = SETTINGS_VAR.RAG_RETRIEVAL_COUNT
    ) -> List[Document]:
        """Delegates similarity search to CRUD module. Returns rich Document objects."""
        return query_collection(self.vector_store, query_text, n_results)

    def count(self) -> int:
        """Delegates document counting to CRUD module."""
        return count_documents(self.vector_store)

    def delete_document_by_name(self, filename: str) -> None:
        """Delegates document deletion to CRUD module."""
        delete_documents_by_metadata(self.vector_store, "source", filename)

    def list_all_metadatas(self) -> List[Dict[str, Any]]:
        """Delegates document listing to CRUD module."""
        return get_all_metadatas(self.vector_store)

    def reset(self) -> None:
        """Resets the collection using the native client."""
        self.vector_store = reset_collection(
            client=self.client,
            collection_name=self.collection_name,
            embedding_fn=self.embedding_fn,
        )


@lru_cache()
def get_chroma_manager() -> ChromaManager:
    return ChromaManager()
