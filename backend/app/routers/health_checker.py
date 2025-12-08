from typing import Dict

from fastapi import APIRouter

health_checker_router = APIRouter()


@health_checker_router.get("/health", tags=["Health"])
async def health_check() -> Dict[str, str]:
    """Simple health check endpoint."""
    return {"status": "ok"}
