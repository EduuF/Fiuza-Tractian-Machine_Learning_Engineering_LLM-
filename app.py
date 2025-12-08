"""main API app file."""

import uvicorn
from fastapi import FastAPI

from backend.app.routers.health_checker import health_checker_router
from backend.app.routers.question_router import question_router
from backend.app.routers.upload_document_router import documents_router

from settings import SETTINGS_VAR

API_HOST = SETTINGS_VAR.API_HOST
API_PORT = SETTINGS_VAR.API_PORT

"""
from app.errors.exception_handlers import (
    swapi_character_error_handler,
    character_not_found_error_handler,
    not_found_error_handler,
    server_error_handler,
    index_out_of_range_error_handler,
)

from app.errors.custom_exceptions import (
    SwapiCharacterError,
    CharacterNotFoundError,
    VehicleNotFoundError,
    SwapiVehicleError,
)
"""

app = FastAPI()

app.include_router(documents_router)
app.include_router(question_router)
app.include_router(health_checker_router)

"""
app.add_exception_handler(SwapiCharacterError, swapi_character_error_handler)
app.add_exception_handler(CharacterNotFoundError, character_not_found_error_handler)
app.add_exception_handler(VehicleNotFoundError, character_not_found_error_handler)
app.add_exception_handler(IndexError, index_out_of_range_error_handler)
app.add_exception_handler(status.HTTP_404_NOT_FOUND, not_found_error_handler)
app.add_exception_handler(status.HTTP_500_INTERNAL_SERVER_ERROR, server_error_handler)
"""

if __name__ == "__main__":
    uvicorn.run("app:app", host=API_HOST, port=API_PORT, reload=True)