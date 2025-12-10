"""
This module contains the high-level business logic (Use Case) for deleting documents.
It orchestrates the removal of data from the Vector Database.
"""

from functools import lru_cache
from typing import Any, Dict

from backend.ChromaDB.chroma_manager import get_chroma_manager
from logs.log_generator import log_message


class DeleteDocumentPipeline:
    """Pipeline responsible for handling document deletion requests."""

    def __init__(self) -> None:
        """Initializes the pipeline dependencies."""
        self.chroma_manager = get_chroma_manager()

    def run(self, filename: str) -> Dict[str, Any]:
        """
        Executes the deletion flow:
        Remove all chunks associated with the filename from ChromaDB.

        Args:
            filename: The unique identifier (source) of the document.

        Returns:
            Dict: Status of the operation.
        """
        log_message(
            f"🗑️ Pipeline: Initiating deletion for document: '{filename}'", "info"
        )

        try:
            self.chroma_manager.delete_document_by_name(filename)

            log_message(
                f"✅ Pipeline: Document '{filename}' successfully deleted.", "info"
            )
            return {"success": True, "id": filename}
        except Exception as e:
            log_message(
                f"❌ Pipeline: Error deleting document '{filename}': {str(e)}", "error"
            )
            return {"success": False, "error": str(e)}


@lru_cache()
def get_delete_document_pipeline() -> DeleteDocumentPipeline:
    return DeleteDocumentPipeline()
