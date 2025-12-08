from typing import List

from fastapi import APIRouter, File, HTTPException, Path, UploadFile, status

from backend.app.schemas.documents_schemas import (
    DocumentDeleteResponse,
    DocumentInfo,
    DocumentUploadResponse,
)
from backend.app.services.documents.delete_document_services import (
    delete_document_service,
)
from backend.app.services.documents.list_documents_services import (
    list_documents_service,
)
from backend.app.services.documents.upload_documents_services import (
    upload_document_service,
)

documents_router = APIRouter()


@documents_router.post(
    "/documents",
    response_model=DocumentUploadResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload PDF documents",
    tags=["Documents"],
)
async def upload_documents(
    files: List[UploadFile] = File(..., description="One or more PDF files")
) -> DocumentUploadResponse:
    """Upload one or more PDF documents to be indexed."""

    # Check if all the files are PDF files
    for file in files:
        if file.content_type != "application/pdf":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File {file.filename} is not a PDF.",
            )

    return upload_document_service(files=files)


@documents_router.get(
    "/documents",
    response_model=List[DocumentInfo],
    status_code=status.HTTP_200_OK,
    summary="List uploaded documents",
    tags=["Documents"],
)
async def list_documents() -> List[DocumentInfo]:
    """List all indexed documents and their metadata."""

    return list_documents_service()


@documents_router.delete(
    "/documents/{doc_id}",
    response_model=DocumentDeleteResponse,
    status_code=status.HTTP_200_OK,
    summary="Delete a document",
    tags=["Documents"],
)
async def delete_document(
    doc_id: str = Path(..., description="The ID of the document to delete")
) -> DocumentDeleteResponse:
    """Delete a specific document by its ID."""

    return delete_document_service(doc_id=doc_id)
