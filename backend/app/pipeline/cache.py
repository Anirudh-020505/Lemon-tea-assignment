import os
import pickle
import numpy as np
from typing import Optional, Dict, Any
from app.ingestion.embedder import LocalEmbedder

CACHE_FILE = "docmind_semantic_cache.pkl"
SIMILARITY_THRESHOLD = 0.88

class SemanticCache:
    _cache: Dict[str, Dict[str, Any]] = {}
    _loaded = False

    @classmethod
    def load_cache(cls):
        if cls._loaded:
            return
        if os.path.exists(CACHE_FILE):
            try:
                with open(CACHE_FILE, "rb") as f:
                    cls._cache = pickle.load(f)
            except Exception as e:
                print(f"Error loading semantic cache, starting fresh: {e}")
                cls._cache = {}
        cls._loaded = True

    @classmethod
    def save_cache(cls):
        try:
            with open(CACHE_FILE, "wb") as f:
                pickle.dump(cls._cache, f)
        except Exception as e:
            print(f"Error saving semantic cache: {e}")

    @classmethod
    def lookup(cls, query: str) -> Optional[str]:
        cls.load_cache()
        if not cls._cache:
            return None

        query_emb = np.array(LocalEmbedder.embed_text(query))
        query_norm = np.linalg.norm(query_emb)
        if query_norm == 0:
            return None

        best_query = None
        best_similarity = -1.0

        for cached_query, cached_data in cls._cache.items():
            cached_emb = np.array(cached_data["embedding"])
            cached_norm = np.linalg.norm(cached_emb)
            if cached_norm == 0:
                continue
                
            similarity = np.dot(query_emb, cached_emb) / (query_norm * cached_norm)
            
            if similarity > best_similarity:
                best_similarity = similarity
                best_query = cached_query

        if best_similarity >= SIMILARITY_THRESHOLD and best_query:
            print(f"[CACHE HIT] Query: '{query}' mapped to cached query: '{best_query}' (Similarity: {best_similarity:.4f})")
            return cls._cache[best_query]["answer"]

        return None

    @classmethod
    def add(cls, query: str, answer: str):
        cls.load_cache()
        try:
            embedding = LocalEmbedder.embed_text(query)
            cls._cache[query] = {
                "answer": answer,
                "embedding": embedding
            }
            cls.save_cache()
        except Exception as e:
            print(f"Error writing to semantic cache: {e}")
