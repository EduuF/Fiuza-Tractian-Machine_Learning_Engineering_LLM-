from backend.app.schemas.question_schemas import QuestionRequest, QuestionResponse
from backend.core.ask_question_pipeline import get_ask_question_pipeline
from logs.log_generator import log_message


def ask_question_services(body: QuestionRequest) -> QuestionResponse:
    """Orchestrates the question-answering flow."""
    # Call question pipeline
    ask_question_pipeline = get_ask_question_pipeline()
    result = ask_question_pipeline.run(body.question)

    ref_count = len(result.get("references", []))
    log_message(
        f"✅ Service: Answer generated based on {ref_count} reference(s) | Answer: {result['answer'][:50]}...",
        "info",
    )

    return QuestionResponse(answer=result["answer"], references=result["references"])
