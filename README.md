# 🧠 RAG API (Fiuza - Tractian)

![Python](https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-Core-green?style=for-the-badge)

A **Retrieval-Augmented Generation (RAG)** system built for the Tractian Machine Learning Engineering Tech Challenge.  
This API allows users to ingest PDF documents and ask context-aware questions using LLM strategies.

---

## 🚀 Key Features

- **RAG Pipeline:** Ingests, chunks, embeds, and retrieves document context.
- **Multi-Provider Strategy:** Implements a **Fallback Pattern** for high availability:
  - **Embedding Models**
    - Primary: OpenAI (text-embedding-3-small)
    - Fallback: Gemini (text-embedding-004)
  - **LLM Models**
    - Primary: OpenAI (GPT-3.5-Turbo)
    - Fallback: Google Gemini (Gemini Pro)
- **Vector Persistence:** Uses **ChromaDB** with persistent storage.
- **Observability:** Colored logging system for improved debugging.
- **Clean Architecture:** Modular separation of concerns.
- **Type Safety:** 100% typed code with `mypy` strict mode.

---

## 🏗️ Architecture

The project structure is inspired by the **FastAPI Reference App** patterns to ensure scalability.

```text
backend/
├── app/                 # API Layer (FastAPI Routers & Schemas)
├── core/                # Business Logic (Pipelines for Ingestion & RAG)
├── ChromaDB/            # Vector Database Manager
│   ├── src/embeddings   # Embedding Strategies (OpenAI / Gemini)
├── LLM/                 # LLM Manager (Strategy Pattern & Factory)
│   ├── prompts/         # YAML Prompts
│   ├── src/models       # OpenAI / Gemini Implementations
└── logs/                # Custom Logger
```

---

## 🛠️ Getting Started

### Prerequisites

- Docker & Docker Compose (recommended)
- Python 3.10+ (for local execution)

### 1. Configuration

Create a `.env` file in the root directory. You can use the `.env.example` file in the root directory as a template:

```
# Keys
OPENAI_API_KEY=
GOOGLE_API_KEY=

# API configuration
API_HOST=localhost
API_PORT=8000

# Chroma DB
CHROMA_DB_PATH=backend/ChromaDB/DB_instance

# Embedding
OPENAI_EMBED_MODEL_NAME=text-embedding-3-small

# LLM
OPENAI_LLM_MODEL_NAME=gpt-3.5-turbo
GOOGLE_LLM_MODEL_NAME=gemini-2.5-flash

# RAG Configs
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
LLM_TEMPERATURE=0.4
RAG_RETRIEVAL_COUNT=5
```

### 2. Running with Docker (Recommended)

This ensures all system dependencies are correctly installed.

```
docker-compose up --build
```

The API will be available at: http://localhost:8000/docs

### 3. Running Locally

If running directly on the host machine:

```
pip install -r requirements.txt
python app.py
```

---

## 📡 Usage

You can interact with the API via the Swagger UI or using `curl`.

### 1. Upload Documents

Uploads and processes a PDF file.

```
curl -X POST "http://localhost:8000/documents" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "files=@yourfile.pdf"
```

### 2. Ask a Question

Performs semantic search and generates an answer using the LLM.

```
curl -X POST "http://localhost:8000/question" \
  -H "Content-Type: application/json" \
  -d '{ "question": "What is the power consumption?" }'
```

### 3. List all Documents

Returns metadata of all indexed files.

```
curl -X GET "http://localhost:8000/documents" \
  -H "Content-Type: application/json"
```

### 4. Delete a Document

Removes all chunks associated with a specific file.

```
curl -X DELETE \
  "http://localhost:8000/documents/{file_name}" \
  -H "accept: application/json"
```

### 5. Health Check

```
curl -X GET \
  "http://localhost:8000/health" \
  -H "accept: application/json"
```

---

## 🧠 Technical Decisions & Trade-offs

### 1. Vector Database: ChromaDB (Local Persistence)
**Decision:** Used ChromaDB in persistent mode via Docker Volumes.
- **Why:** It eliminates the operational overhead of maintaining external VMs or managed vector services for a standalone challenge  while keeping the infrastructure portable and self-contained.

### 2. Concurrency Control: Singleton Pattern
**Decision:** The Database Coordinator (`ChromaManager`) is instantiated as a strict Singleton using `@lru_cache`.
- **Why:** Since we are running ChromaDB locally, multiple uncoordinated instances trying to write to the same directory could lead to **race conditions** or database locks. The Singleton pattern ensures a single point of entry for all DB operations.

### 3. Resilience: Strategy Pattern & Fallbacks
**Decision:** Implemented Abstract Factories for both Embeddings and LLMs.
- **Why:** To ensure high availability.
    - **Embedding:** Tries OpenAI first; if it fails (Auth/Connection), falls back to Google Gemini model (`text-embedding-004`).
    - **Generation:** Tries OpenAI (`gpt-3.5`) first; if it fails, falls back to Google Gemini (`gemini-pro`).

### 4. Configuration: Pydantic Settings
**Decision:** All configuration is managed via `pydantic-settings`.
- **Why:** It provides type validation for environment variables.

### 5. Modular Architecture Style
**Decision:** To maintain clear separation between the API Interface (Routers), Business Logic (Services/Pipelines), Data Access Layers and LLM Module. A module only knows the interface of another module, not its implementation.

---

## 🧪 Quality Assurance

To ensure code quality, a linting pipeline is included. It runs:
- **Isort:** Sorts imports.
- **Black:** Formats code.
- **Flake8:** Enforces style.
- **MyPy:** Checks static types.

Run locally via PowerShell:

```
./lint.ps1
```  

---

## 🔮 Future Improvements

- Async background workers for ingestion  
- RAG Evaluation: Ragas / TruLens
- Persistent log files for later comparisons and improvement tracking.
- Custom and General Exception Handlers

---