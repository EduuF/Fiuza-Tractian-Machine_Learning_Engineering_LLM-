from backend.app.schemas.documents_schemas import DocumentDeleteResponse


def delete_document_service(doc_id: str) -> DocumentDeleteResponse:
    # TODO: Chamar service para remover do Chroma os chunks relacionados a este doc

    return DocumentDeleteResponse(message="Document deleted successfully", id=doc_id)
