"""Service for listing all the documents in ChromaDB."""

from typing import List

from backend.app.schemas.documents_schemas import DocumentInfo
from backend.core.loaded_pdfs_pipeline import get_loaded_pdfs_pipeline
from logs.log_generator import log_message


def list_documents_service() -> List[DocumentInfo]:
    """Orchestrates the retrieval of indexed documents."""
    # Call listing loaded pdfs piepline
    loaded_pdfs_pipeline = get_loaded_pdfs_pipeline()
    docs_data = loaded_pdfs_pipeline.run()

    log_message(
        f"⚙️ Service: Retrieved metadata for {len(docs_data)} document(s).", "info"
    )

    # Mapping to pydantic schema
    response_list = []
    for doc in docs_data:
        response_list.append(
            DocumentInfo(
                id=doc["id"],
                filename=doc["filename"],
                upload_date=doc["upload_date"],
                content_type=doc["content_type"],
                size=doc["size"],
            )
        )

    return response_list
