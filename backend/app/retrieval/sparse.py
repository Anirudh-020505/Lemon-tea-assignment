import re
import asyncpg
from typing import List, Dict, Tuple
from rank_bm25 import BM25Okapi
from app.database import get_pool
from app.pipeline.state import DocumentChunk

class SparseRetriever:
    _bm25: BM25Okapi = None
    _corpus_map: List[asyncpg.Record] = []
    _loaded = False
    
    @staticmethod
    def _tokenize(text: str) -> List[str]:
        return re.findall(r'\b\w+\b', text.lower())

    @classmethod
    async def load_index(cls):
        pool = get_pool()
        async with pool.acquire() as conn:
            cls._corpus_map = await conn.fetch("SELECT id, doc_id, content, page_num, metadata FROM chunks")
            
        corpus_tokens = [cls._tokenize(row["content"]) for row in cls._corpus_map]
        
        if corpus_tokens:
            cls._bm25 = BM25Okapi(corpus_tokens)
        else:
            cls._bm25 = None
            
        cls._loaded = True

    @classmethod
    async def retrieve(cls, query: str, top_k: int = 10) -> List[DocumentChunk]:
        if not cls._loaded:
            await cls.load_index()
            
        if not cls._bm25 or not cls._corpus_map:
            return []

        query_tokens = cls._tokenize(query)
        scores = cls._bm25.get_scores(query_tokens)
        
        results = list(zip(cls._corpus_map, scores))
        results.sort(key=lambda x: x[1], reverse=True)
        
        valid_results = [item for item in results[:top_k] if item[1] > 0.0]
        
        chunks = []
        import json
        for row, score in valid_results:
            meta = row["metadata"]
            if isinstance(meta, str):
                try:
                    meta = json.loads(meta)
                except:
                    meta = {}
            elif not isinstance(meta, dict):
                meta = {}
                
            chunks.append(DocumentChunk(
                id=str(row["id"]),
                document_id=str(row["doc_id"]),
                content=row["content"],
                page_number=row["page_num"] or 1,
                score=float(score),
                metadata=meta
            ))
            
        return chunks
