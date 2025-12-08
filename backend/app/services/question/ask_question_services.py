from backend.app.schemas.question_schemas import QuestionRequest, QuestionResponse


def ask_question_services(body: QuestionRequest) -> QuestionResponse:
    # TODO: Lógica principal do RAG
    # 1 - Converter body.question em embedding (vetor)
    # 2 - Buscar chunks similares no ChromaDB (Retrieval)
    # 3 - Montar o prompt com os chunks encontrados
    # 4 - Enviar para a LLM (OpenAI/Anthropic/Local) gerar a resposta

    # Mockando a resposta conforme exemplo do PDF para validar a interface da API

    return QuestionResponse(
        answer="The motor's power consumption is 2.3 kW.",
        references=[
            "the motor xxx has requires 2.3kw to operate at a 60hz line frequency"
        ],
    )
