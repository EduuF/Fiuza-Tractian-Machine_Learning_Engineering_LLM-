"""Main FastAPI Application Entry Point."""

import uvicorn
from fastapi import FastAPI

from backend.app.routers.health_checker import health_checker_router
from backend.app.routers.question_router import question_router
from backend.app.routers.upload_document_router import documents_router
from logs.log_generator import log_message
from settings import SETTINGS_VAR

app = FastAPI(
    title="Tractian Challenge - RAG API",
    description="API for Document Ingestion and Retrieval Augmented Generation",
    version="1.0.0",
)

app.include_router(documents_router)
app.include_router(question_router)
app.include_router(health_checker_router)

if __name__ == "__main__":
    log_message("Booting API...", "info")
    uvicorn.run(
        "app:app", host=SETTINGS_VAR.API_HOST, port=SETTINGS_VAR.API_PORT, reload=False
    )
