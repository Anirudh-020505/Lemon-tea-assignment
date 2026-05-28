import asyncio
from app.database import connect_db, disconnect_db, get_pool

async def main():
    await connect_db()
    pool = get_pool()
    async with pool.acquire() as conn:
        doc_count = await conn.fetchval("SELECT COUNT(*) FROM documents")
        chunk_count = await conn.fetchval("SELECT COUNT(*) FROM chunks")
        emb_count = await conn.fetchval("SELECT COUNT(*) FROM embeddings")
        
        print(f"Documents: {doc_count}")
        print(f"Chunks: {chunk_count}")
        print(f"Embeddings: {emb_count}")
        
        docs = await conn.fetch("SELECT id, name, status, chunk_count FROM documents")
        for d in docs:
            print(f"Doc: {dict(d)}")
            
        chunks = await conn.fetch("SELECT id, doc_id, chunk_index, length(content) as len FROM chunks LIMIT 5")
        for c in chunks:
            print(f"Chunk: {dict(c)}")
            
    await disconnect_db()

if __name__ == "__main__":
    asyncio.run(main())
