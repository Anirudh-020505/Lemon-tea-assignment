import asyncpg
from typing import List
from app.database import get_pool
from app.pipeline.state import DocumentChunk
from app.ingestion.embedder import Embedder

class DenseRetriever:
    @staticmethod
    async def retrieve(query: str, top_k: int = 10) -> List[DocumentChunk]:
        embedder = Embedder()
        query_vector = await embedder.embed_text(query)
        
        pool = get_pool()
        
        sql = """
            SELECT 
                c.id, 
                c.doc_id, 
                c.content, 
                c.page_num,
                c.metadata,
                (1 - (e.embedding <=> $1::vector)) AS score
            FROM chunks c
            JOIN embeddings e ON c.id = e.chunk_id
            ORDER BY e.embedding <=> $1::vector
            LIMIT $2;
