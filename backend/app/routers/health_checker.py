"""API ealth Checker endpoint."""

from typing import Dict

from fastapi import APIRouter

from logs.log_generator import log_message

health_checker_router = APIRouter()


@health_checker_router.get("/health", tags=["Health"])
async def health_check() -> Dict[str, str]:
    """Simple health check endpoint."""
    log_message("Health check probe received.", "info")
    return {"status": "ok"}
