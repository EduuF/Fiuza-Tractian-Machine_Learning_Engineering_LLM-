"""Question maker route."""

from fastapi import APIRouter, status

from backend.app.schemas.question_schemas import QuestionRequest, QuestionResponse
from backend.app.services.question.ask_question_services import ask_question_services
from logs.log_generator import log_message

question_router = APIRouter()


@question_router.post(
    "/question",
    response_model=QuestionResponse,
    status_code=status.HTTP_200_OK,
    summary="Ask a question based on uploaded documents",
    tags=["Question"],
)
async def ask_question(body: QuestionRequest) -> QuestionResponse:
    """Ask questions based on the uploaded content."""
    log_message(f"📥 API Request: Received question: '{body.question}'", "info")
    return ask_question_services(body=body)
