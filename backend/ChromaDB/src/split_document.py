"""
This module is responsible for processing raw PDF files into manageable text chunks.
It handles both text extraction and smart splitting based on configured settings.
"""

import io
from typing import Any, Dict, List

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from pypdf import PdfReader

from logs.log_generator import log_message
from settings import SETTINGS_VAR


class DocumentProcessor:
    def __init__(
        self,
        chunk_size: int = SETTINGS_VAR.CHUNK_SIZE,
        chunk_overlap: int = SETTINGS_VAR.CHUNK_OVERLAP,
    ) -> None:
        """Initializes the text splitter with configuration from settings."""
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            is_separator_regex=False,
        )

    def _extract_documents_from_bytes(
        self, file_bytes: bytes, base_metadata: Dict[str, Any]
    ) -> List[Document]:
        """
        Extracts text from PDF bytes, preserving page metadata.
        Returns a list of LangChain Documents (one per page).
        """
        try:
            pdf_stream = io.BytesIO(file_bytes)
            reader = PdfReader(pdf_stream)
            documents = []

            for i, page in enumerate(reader.pages):
                text = page.extract_text()
                if text:
                    doc = Document(
                        page_content=text,
                        metadata={**base_metadata, "page_number": i + 1},
                    )
                    documents.append(doc)

            return documents
        except Exception as e:
            log_message(f"❌ Processor: Error reading PDF stream: {e}", "error")
            return []

    def process_file(
        self, file_bytes: bytes, metadata: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Orchestrates extraction and splitting.
        Returns a list of chunk dictionaries ready for DB insertion.
        """
        # Extract Documents
        page_docs = self._extract_documents_from_bytes(file_bytes, metadata)

        if not page_docs:
            log_message("⚠️ Processor: No text extracted from file.", "warning")
            return []

        # Split into chunks
        chunks = self.text_splitter.split_documents(page_docs)

        processed_chunks = []
        for i, chunk in enumerate(chunks):
            chunk_id = f"{metadata.get('source', 'doc')}_p{chunk.metadata.get('page_number')}_{i}"

            chunk_data = {
                "id": chunk_id,
                "text": chunk.page_content,
                "metadata": chunk.metadata,
            }
            processed_chunks.append(chunk_data)

        return processed_chunks
