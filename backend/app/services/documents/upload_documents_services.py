from typing import List
from fastapi import UploadFile, File

from backend.app.schemas.documents_schemas import DocumentUploadResponse


def upload_document_service(files: List[UploadFile] = File(...,)) -> DocumentUploadResponse:
    # TODO: Processa, extrai texto e salva no ChromaDB
    return DocumentUploadResponse(
        message="Documents processed successfully",
        documents_indexed=len(files),
        total_chunks=0
    )