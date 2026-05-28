import os
import pytest
from app.pipeline.cache import SemanticCache, CACHE_FILE
from app.pipeline.graph import rag_graph

def test_semantic_cache_add_and_lookup():
    if os.path.exists(CACHE_FILE):
        try:
            os.remove(CACHE_FILE)
        except:
            pass
            
    SemanticCache._cache = {}
    SemanticCache._loaded = False
    
    query = "What is the capital of France?"
    answer = "The capital of France is Paris."
    
    SemanticCache.add(query, answer)
    
    match = SemanticCache.lookup(query)
    assert match == answer
    
    similar_query = "What is capital of France"
    match_similar = SemanticCache.lookup(similar_query)
    assert match_similar == answer
    
    unrelated_query = "How to boil an egg?"
    match_unrelated = SemanticCache.lookup(unrelated_query)
    assert match_unrelated is None

def test_langgraph_compilation():
    assert rag_graph is not None
    assert hasattr(rag_graph, "ainvoke")
    node_names = list(rag_graph.nodes.keys())
    assert "retrieve" in node_names
    assert "rerank" in node_names
    assert "grade" in node_names
    assert "rewrite" in node_names
    assert "generate" in node_names
