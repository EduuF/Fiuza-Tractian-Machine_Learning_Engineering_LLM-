"""Service for document deletion from ChromaDB."""

from typing import List, Tuple

from fastapi import File, UploadFile

from backend.app.schemas.documents_schemas import DocumentUploadResponse
from backend.core.upload_pdf_pipeline import get_upload_pdf_pipeline
from logs.log_generator import log_message


async def upload_document_service(
    files: List[UploadFile] = File(...),
) -> DocumentUploadResponse:
    """Orchestrates the reading of uploaded files and calls the ingestion pipeline."""
    log_message("⚙️ Service: Starting document preparation.", "info")

    prepared_documents: List[Tuple[str, bytes, str]] = []

    for file in files:
        try:
            # UploadFile is async
            content = await file.read()
            file_size_kb = len(content) / 1024

            safe_filename: str = (
                str(file.filename) if file.filename else "unknown_file.pdf"
            )
            safe_content_type: str = (
                str(file.content_type) if file.content_type else "application/pdf"
            )

            log_message(
                f"📖 Read file '{safe_filename}' ({file_size_kb:.2f} KB).", "info"
            )

            prepared_documents.append((safe_filename, content, safe_content_type))
        except Exception as e:
            fname = file.filename or "unknown"
            log_message(f"❌ Failed to read file '{fname}': {str(e)}", "error")

    # There is no valid document? Return
    if not prepared_documents:
        log_message("⚠️ No valid documents to process.", "warning")
        return DocumentUploadResponse(documents_indexed=0, total_chunks=0)

    # Call upload documents pipeline
    log_message(
        f"🚀 Service: Delegating {len(prepared_documents)} files to LoadPDFPipeline.",
        "info",
    )
    load_pdf_pipeline = get_upload_pdf_pipeline()
    loading_response = load_pdf_pipeline.run(prepared_documents)

    # Log summary from pipeline response
    success_count = loading_response.get("success_count", 0)
    failed_count = loading_response.get("failed_count", 0)

    if failed_count > 0:
        log_message(
            f"⚠️ Service completed with issues. Indexed: {success_count}, Failed: {failed_count}",
            "warning",
        )
    else:
        log_message(
            f"✅ Service completed successfully. Indexed: {success_count} documents.",
            "info",
        )

    return DocumentUploadResponse(
        documents_indexed=len(loading_response["successful_files"]),
        total_chunks=loading_response["total_chunks_added"],
    )
