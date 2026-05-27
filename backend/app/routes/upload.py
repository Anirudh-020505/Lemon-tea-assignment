import os
from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from app.database import get_pool
from app.ingestion.parser import DocumentParser
from app.ingestion.chunker import RecursiveCharacterChunker
from app.ingestion.embedder import Embedder

router = APIRouter()

UPLOAD_DIR = "./data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def process_document(file_path: str, filename: str, doc_id: str):
    pool = get_pool()
    try:
        text_content = DocumentParser.parse(file_path)
        if not text_content.strip():
            raise ValueError("No readable text found.")
            
        chunker = RecursiveCharacterChunker()
        text_chunks = chunker.chunk(text_content)
        
        if not text_chunks:
            raise ValueError("Chunking resulted in 0 chunks.")
            
        async with pool.acquire() as conn:
            await conn.execute("UPDATE documents SET chunk_count = $1, status = 'embedding' WHERE id = $2", len(text_chunks), doc_id)
            
        embedder = Embedder()
        vectors = await embedder.embed_texts(text_chunks)
        if len(vectors) != len(text_chunks):
            vectors = []
            for chunk in text_chunks:
                vec = await embedder.embed_text(chunk)
                vectors.append(vec)
        
        async with pool.acquire() as conn:
            async with conn.transaction():
                for i, (chunk, vector) in enumerate(zip(text_chunks, vectors)):
                    chunk_id = await conn.fetchval("""
                        INSERT INTO chunks (doc_id, content, chunk_index, chunk_type)
                        VALUES ($1, $2, $3, 'text')
                        RETURNING id
                        INSERT INTO embeddings (chunk_id, embedding)
                        VALUES ($1, $2::vector)
    Ingests a document and queues it for background processing.
                INSERT INTO documents (name, file_type, size_bytes, status)
                VALUES ($1, $2, $3, 'processing')
                RETURNING id
