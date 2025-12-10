"""Service for document deletion from ChromaDB."""

from fastapi import HTTPException, status

from backend.app.schemas.documents_schemas import DocumentDeleteResponse
from backend.core.delete_document_pipeline import get_delete_document_pipeline
from logs.log_generator import log_message


def delete_document_service(doc_id: str) -> DocumentDeleteResponse:
    """Orchestrates the deletion of a document via the pipeline."""
    log_message(f"⚙️ Service: Initiating deletion for document ID: {doc_id}", "info")

    # Call deletion pipeline
    delete_document_pipeline = get_delete_document_pipeline()
    result = delete_document_pipeline.run(doc_id)

    if not result.get("success"):
        error_msg = result.get("error")
        log_message(f"❌ Service: Deletion failed. Reason: {error_msg}", "error")

        # If the pipeline failed (database error for example), raise HTTP 500
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete document: {error_msg}",
        )

    log_message(f"✅ Service: Document {doc_id} deleted successfully.", "info")

    return DocumentDeleteResponse(
        message="Document chunks deleted successfully from Vector Store", id=doc_id
    )
