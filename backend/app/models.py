from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID


class DocumentResponse(BaseModel):
    id: UUID
    name: str
    file_type: str
    size_bytes: int
    uploaded_at: datetime
    chunk_count: int
    status: str

    model_config = {
        "from_attributes": True
    }

class QueryRequest(BaseModel):
    query: str = Field(..., description="The search query from the user")
    
class QueryResponse(BaseModel):
    answer: str
    confidence_score: int
    citations_verified: bool
    context_chunks: List[Dict[str, Any]]

class ChunkMetadata(BaseModel):
    id: UUID
    doc_id: UUID
    content: str
    chunk_index: int
    page_num: Optional[int]
    chunk_type: str
    metadata: Dict[str, Any]
    score: Optional[float] = None
