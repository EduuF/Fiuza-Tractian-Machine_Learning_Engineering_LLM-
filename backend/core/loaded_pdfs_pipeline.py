"""
This module contains the logic to retrieve and aggregate document information
from the vector database.
"""

from functools import lru_cache
from typing import Any, Dict, List

from backend.ChromaDB.chroma_manager import get_chroma_manager
from logs.log_generator import log_message


class LoadedPDFsPipeline:
    """Pipeline responsible for aggregating chunk metadata into a document list."""

    def __init__(self) -> None:
        self.chroma_manager = get_chroma_manager()

    def run(self) -> List[Dict[str, Any]]:
        """
        Retrieves all chunks metadata and groups them by document source.

        Returns:
            List of dictionaries representing unique documents with their stats.
        """
        log_message(
            "📊 Pipeline: Aggregating metadata for all loaded documents...", "info"
        )

        raw_metadatas = self.chroma_manager.list_all_metadatas()

        docs_map: Dict[str, Dict[str, Any]] = {}

        for meta in raw_metadatas:
            if not meta:
                continue

            source = meta.get("source")
            if not source:
                continue

            if source not in docs_map:
                docs_map[source] = {
                    "id": source,
                    "filename": source,
                    "total_chunks": 0,
                    # Fallback values if metadata is missing
                    "size": meta.get("file_size", 0),
                    "upload_date": meta.get("upload_date", ""),
                    "content_type": meta.get("content_type", "application/pdf"),
                }

            docs_map[source]["total_chunks"] += 1

        unique_count = len(docs_map)
        log_message(f"✅ Pipeline: Found {unique_count} unique document(s).", "info")

        return list(docs_map.values())


@lru_cache()
def get_loaded_pdfs_pipeline() -> LoadedPDFsPipeline:
    return LoadedPDFsPipeline()
