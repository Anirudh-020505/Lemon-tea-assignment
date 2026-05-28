from typing import List, Dict, Any, Optional
from typing_extensions import TypedDict

class RouterOutput(TypedDict):
    complexity: str 
    reasoning_effort: str 

class DocumentChunk(TypedDict):
    id: str
    document_id: str
    content: str
    page_number: int
    score: float 
    metadata: Dict[str, Any]

class GraphState(TypedDict):
    query: str
    reasoning_effort: str 
    expanded_queries: List[str] 
    
    raw_chunks: List[DocumentChunk] 
    fused_chunks: List[DocumentChunk] 
    reranked_chunks: List[DocumentChunk] 
    final_context: List[DocumentChunk] 
    
    loop_count: int 
    context_sufficient: bool 
    
    generation: str 
    confidence_score: int 
    citations_verified: bool 
