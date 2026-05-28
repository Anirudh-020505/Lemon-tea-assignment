# DocMind: Multi-Document Enterprise Search Assistant

> **Assignment Submission:** Software Development Intern – Full Stack & Gen-AI
> **Track:** Multi-Document Enterprise Search Assistant

DocMind is an advanced, production-ready Retrieval-Augmented Generation (RAG) system. It allows users to upload multiple enterprise documents (PDFs, TXT) and performs intelligent, context-aware queries across the entire knowledge base.

Unlike basic RAG tutorials, DocMind implements an **Agentic Hybrid-Search Pipeline** using LangGraph, combining dense vector search, sparse keyword search, and cross-encoder reranking to achieve state-of-the-art retrieval accuracy.

---

## a. Setup Instructions

### Prerequisites
- Python 3.10+
- Node.js 20+
- OpenAI API Key
- Neon PostgreSQL Database (with `pgvector` enabled)

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Environment Variables:
   Copy `.env.example` to `.env` and fill in your keys:
   ```env
   OPENAI_API_KEY=your_openai_key
   DATABASE_URL=postgresql://user:pass@ep-host.aws.neon.tech/neondb?sslmode=require
   ```
5. Run the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install Node dependencies:
   ```bash
   npm install
   ```
3. Run the Vite development server:
   ```bash
   npm run dev
   ```
4. Open your browser at `http://localhost:5173`.

---

## b. Architecture Overview

DocMind is a decoupled Full-Stack application:
1. **Frontend**: Built with React and Vite. It utilizes a custom `useSSE` hook to consume real-time Server-Sent Events, rendering a transparent "Reasoning Trace" and streaming the LLM response token-by-token.
2. **Backend**: Built with FastAPI. It handles async HTTP requests and manages the connection pool to the database.
3. **Database**: Neon PostgreSQL. It stores document metadata relationally and uses the `pgvector` extension to store and index 1536-dimensional chunk embeddings.
4. **AI Pipeline (LangGraph)**: The RAG logic is modeled as a stateful directed graph. 
   - **Retrievers**: `text-embedding-3-large` (Dense) + `rank-bm25` (Sparse).
   - **Reranker**: `flashrank` local Cross-Encoder.
   - **Generator**: `gpt-5.5-2026-04-23` (LLM).

---

## c. Design Decisions

- **Hybrid Search + Reranking**: Standard dense vector search often fails on domain-specific acronyms or exact keyword matches. DocMind runs Dense and Sparse searches in parallel, merges the results, and uses a Cross-Encoder to re-score them. This guarantees extremely high retrieval precision.
- **Agentic Orchestration (LangGraph)**: Instead of a linear script, the RAG pipeline is a state machine. This allows the system to easily implement cyclic logic in the future (e.g., if confidence is low, loop back and rewrite the query). It also allows the backend to stream exact internal state changes ("Reasoning Traces") to the UI.
- **Server-Sent Events (SSE)**: Rather than WebSockets (which are heavy and stateful), SSE was chosen because LLM generation is a unidirectional data flow (Server → Client). SSE natively supports HTTP/2 multiplexing and works flawlessly behind serverless proxies.
- **Unified Postgres (Neon)**: We avoided using a separate Vector DB (like Pinecone). Using Neon with `pgvector` allows us to enforce referential integrity (`ON DELETE CASCADE`) between a Document and its Vector Chunks, drastically simplifying data management.

---

## d. Assumptions Made

1. **Document Types**: The system currently assumes documents are text-heavy (PDFs/MD/TXT). Advanced OCR for images/diagrams inside PDFs is outside the current scope.
2. **In-Memory Sparse Index**: `rank-bm25` computes the sparse index in-memory. For a massive enterprise deployment (terabytes of data), this specific component would be migrated to Postgres Full-Text Search or Elasticsearch.
3. **Confidence Scoring**: The hallucination/confidence check currently relies on deterministic citation matching (verifying if the LLM successfully cited the provided chunk IDs).

---

## API Documentation

FastAPI automatically generates interactive Swagger documentation available at `http://localhost:8000/docs`.

### Core Endpoints:

#### `POST /api/upload`
- **Description**: Uploads a document (PDF/TXT). Parses the text, splits it into semantic chunks, generates embeddings via OpenAI, and stores everything in Neon Postgres.
- **Payload**: `multipart/form-data` (file)
- **Response**: `{ "id": "uuid", "filename": "doc.pdf", "chunks": 42 }`

#### `GET /api/documents`
- **Description**: Retrieves a list of all uploaded documents and their processing status.
- **Response**: `[ { "id": "uuid", "name": "doc.pdf", "size_bytes": 1024, "chunk_count": 42 } ]`

#### `DELETE /api/documents/{doc_id}`
- **Description**: Deletes a document. Due to `ON DELETE CASCADE` in the schema, all associated chunks and embeddings are automatically wiped from the vector database.

#### `GET /api/query`
- **Description**: The core RAG endpoint. Accepts a user query and returns a streaming `text/event-stream` (SSE).
- **Query Parameter**: `question` (string)
- **Event Types Emitted**:
  - `trace`: LangGraph state changes (e.g., "Retrieved 15 chunks").
  - `docs`: The final reranked context documents sent to the LLM.
  - `token`: Streamed words from the LLM for typewriter-effect rendering.
  - `score`: Confidence evaluation of the final answer.
