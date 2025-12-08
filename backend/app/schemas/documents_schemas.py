from pydantic import BaseModel
from datetime import datetime

class DocumentUploadResponse(BaseModel):
    message: str
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