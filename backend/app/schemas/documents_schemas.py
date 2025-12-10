"""Basemodel schemas for documents."""

from datetime import datetime

from pydantic import BaseModel


class DocumentUploadResponse(BaseModel):
    documents_indexed: int
    total_chunks: int


class DocumentInfo(BaseModel):
    id: str
    filename: str
    upload_date: datetime
    content_type: str
    size: int


class DocumentDeleteResponse(BaseModel):
    message: str
    id: str
