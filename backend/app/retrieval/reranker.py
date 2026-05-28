import os
from typing import List, Dict, Any
from flashrank import Ranker, RerankRequest
from app.pipeline.state import DocumentChunk

class FlashRankReranker:
    _ranker: Ranker = None
    
    @classmethod
    def get_ranker(cls):
        if cls._ranker is None:
            cache_dir = os.path.join(os.getcwd(), "flashrank_cache")
            os.makedirs(cache_dir, exist_ok=True)
            cls._ranker = Ranker(model_name="ms-marco-MiniLM-L-12-v2", cache_dir=cache_dir)
        return cls._ranker

    @classmethod
    def rerank(cls, query: str, candidates: List[DocumentChunk], top_k: int = 6) -> List[DocumentChunk]:
        if not candidates:
            return []
            
        ranker = cls.get_ranker()
        
        passages = []
        for doc in candidates:
            passages.append({
                "id": doc["id"],
                "text": doc["content"],
                "meta": {
                    "document_id": doc["document_id"],
                    "page_number": doc["page_number"],
                    "metadata": doc["metadata"]
                }
            })
            
        rerankrequest = RerankRequest(query=query, passages=passages)
        results = ranker.rerank(rerankrequest)
        
        reranked_chunks = []
        for res in results[:top_k]:
            reranked_chunks.append(DocumentChunk(
                id=res["id"],
                document_id=res["meta"]["document_id"],
                content=res["text"],
                page_number=res["meta"]["page_number"],
                score=float(res.get("score", 0.0)),
                metadata=res["meta"]["metadata"]
            ))
            
        return reranked_chunks
