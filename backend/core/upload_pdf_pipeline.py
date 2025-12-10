"""
This module contains the high-level business logic (Use Case) for ingesting documents.
It orchestrates the DocumentProcessor and the ChromaManager.
It is completely agnostic of the API framework (FastAPI).
"""

import time
from datetime import datetime
from functools import lru_cache
from typing import Any, Dict, List, Tuple

from backend.ChromaDB.chroma_manager import get_chroma_manager
from backend.ChromaDB.src.split_document import DocumentProcessor
from logs.log_generator import log_message


class UpoadPDFPipeline:
    """Pipeline responsible for the end-to-end ingestion process of PDF documents."""

    def __init__(self) -> None:
        """Initializes the pipeline dependencies (Database & Processor)."""
        self.chroma_manager = get_chroma_manager()
        self.processor = DocumentProcessor()

    def run(self, documents: List[Tuple[str, bytes, str]]) -> Dict[str, Any]:
        """
        Executes the ingestion flow for a batch of documents:
        1 - Clean up existing records.
        2 - Create Metadata.
        3 - Extract & Chunk.
        4 - Persist to DB.

        Args:
            documents: List of tuples (filename, file_bytes, content_type).

        Returns:
            Dict: Statistics about the batch operation.
        """
        total_chunks = 0
        successful_docs = []
        failed_docs = []

        log_message(
            f"🚀 Pipeline: Starting batch ingestion for {len(documents)} document(s).",
            "info",
        )

        for filename, file_bytes, content_type in documents:
            try:
                # Removing old data for this file to prevent duplicates.
                log_message(
                    f"🚀 Pipeline: Searching for older reference for {filename} in database.",
                    "info",
                )
                self.chroma_manager.delete_document_by_name(filename)

                file_metadata = {
                    "source": filename,
                    "file_size": len(file_bytes),
                    "upload_timestamp": time.time(),
                    "upload_date": datetime.now().isoformat(),
                    "content_type": content_type,
                }

                chunks = self.processor.process_file(
                    file_bytes=file_bytes, metadata=file_metadata
                )

                if not chunks:
                    log_message(
                        f"⚠️ Pipeline: File '{filename}' resulted in 0 chunks (empty or unreadable).",
                        "warning",
                    )
                    failed_docs.append(
                        {"filename": filename, "error": "No text extracted"}
                    )
                    continue

                self.chroma_manager.add_chunks(chunks)

                count = len(chunks)
                total_chunks += count
                successful_docs.append(filename)
                log_message(
                    f"✅ Pipeline: Document '{filename}' ingested successfully ({count} chunks).",
                    "info",
                )

            except Exception as e:
                log_message(
                    f"❌ Pipeline: Error processing '{filename}': {str(e)}", "error"
                )
                failed_docs.append({"filename": filename, "error": str(e)})

        return {
            "success_count": len(successful_docs),
            "failed_count": len(failed_docs),
            "total_chunks_added": total_chunks,
            "successful_files": successful_docs,
            "failed_files": failed_docs,
        }


@lru_cache()
def get_upload_pdf_pipeline() -> UpoadPDFPipeline:
    return UpoadPDFPipeline()
