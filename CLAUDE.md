# CLAUDE.md

## Build & Run Commands

### Backend (FastAPI)
- **Install dependencies**: `pip install -r backend/requirements.txt`
- **Run dev server**: `uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000`
- **Active env copy**: `cp backend/.env.example backend/.env`

### Frontend (Vite & React)
- **Install dependencies**: `npm --prefix frontend install`
- **Run dev server**: `npm --prefix frontend run dev`
- **Build production bundle**: `npm --prefix frontend run build`

## Code Verification & Testing
- **Run all unit tests**: `pytest tests/` (from the root or backend directory)
- **Run specific test file**: `pytest tests/test_pipeline.py`

## Project Architecture Guideline
- Backend uses **FastAPI** on port `8000` with endpoints starting with `/api`.
- Database operations use **SQLAlchemy** connected to a local SQLite database (`docmind.db`).
- Ingestion converts PDF/Markdown/TXT files into embeddings via `all-MiniLM-L6-v2` locally.
- RAG Graph transitions are modeled using **LangGraph**.
- Streaming uses Server-Sent Events (SSE) via `EventSource` on the client.
- Frontend styling uses vanilla CSS modules/variables in `index.css` following dark-mode glassmorphic themes.
- Coding style: Keep code clean, explicit type-hints in Python, async-await for standard FastAPI endpoints, and hooks for React logic.
