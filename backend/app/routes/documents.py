from fastapi import APIRouter, HTTPException
from app.database import get_pool
from app.models import DocumentResponse

router = APIRouter()

@router.get("/documents", response_model=list[DocumentResponse])
async def list_documents():
    pool = get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch("SELECT id, name, file_type, size_bytes, uploaded_at, chunk_count, status FROM documents ORDER BY uploaded_at DESC")
        
    docs = []
    for row in rows:
        docs.append(DocumentResponse(
            id=row["id"],
            name=row["name"],
            file_type=row["file_type"],
            size_bytes=row["size_bytes"] or 0,
            uploaded_at=row["uploaded_at"],
            chunk_count=row["chunk_count"] or 0,
            status=row["status"]
        ))
        
    return docs

@router.delete("/documents/{doc_id}")
async def delete_document(doc_id: str):
    pool = get_pool()
    async with pool.acquire() as conn:
        deleted = await conn.execute("DELETE FROM documents WHERE id = $1::uuid", doc_id)
        
    if deleted == "DELETE 0":
        raise HTTPException(status_code=404, detail="Document not found")
        
    return {
        "status": "success",
        "message": "Successfully deleted document."
    }
