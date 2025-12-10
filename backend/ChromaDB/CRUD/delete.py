"""
This module handles deletion operations within the ChromaDB collection.
It provides functions to delete specific documents by metadata or reset the entire database.
"""

from chromadb import ClientAPI
from langchain_chroma import Chroma
from langchain_core.embeddings import Embeddings

from logs.log_generator import log_message


def delete_documents_by_metadata(
    vector_store: Chroma, metadata_key: str, metadata_value: str
) -> None:
    """
    Deletes specific documents (chunks) from the Vector Store based on a metadata filter.
    !!Only logs success if documents were actually found and deleted.!!

    Args:
        vector_store: The LangChain Chroma instance.
        metadata_key: The metadata field to filter by (e.g., "source").
        metadata_value: The value to match (e.g., "contract.pdf").
    """
    # Check if documents exist first
    existing_docs = vector_store._collection.get(
        where={metadata_key: metadata_value}, include=[]
    )

    found_ids = existing_docs.get("ids", [])
    count = len(found_ids)

    if count == 0:
        log_message(
            f"✅ CRUD: No chunks found to delete where {metadata_key} == '{metadata_value}'",
            "info",
        )
        return

    # Delete if data exists
    vector_store._collection.delete(where={metadata_key: metadata_value})

    log_message(
        f"🗑️ CRUD: Successfully deleted {count} chunk(s) where {metadata_key} == '{metadata_value}'",
        "info",
    )


def reset_collection(
    client: ClientAPI, collection_name: str, embedding_fn: Embeddings
) -> Chroma:
    """
    Resets the database by deleting and recreating the collection.
    This is mainly used when the embedding model is changed so the dimensionality is also changed so we gotta reset the DB.

    Args:
        client: The native ChromaDB Client (Persistent).
        collection_name: The name of the collection to reset.
        embedding_fn: The embedding function to reuse for the new collection.

    Returns:
        Chroma: A fresh LangChain wrapper around the new collection.
    """
    try:
        client.delete_collection(collection_name)
        log_message(
            f"⚠️ CRUD: Collection '{collection_name}' has been deleted (reset).",
            "warning",
        )
    except Exception as e:
        log_message(
            f"❌ CRUD: Error deleting collection during reset (it might not exist): {e}",
            "warning",
        )

    log_message(f"🆕 CRUD: Re-initializing collection '{collection_name}'...", "info")
    return Chroma(
        client=client, collection_name=collection_name, embedding_function=embedding_fn
    )
