import asyncpg          

from app.config import get_settings 

_pool: asyncpg.Pool | None = None


async def connect_db() -> None:
    global _pool                         
    settings = get_settings()
    _pool = await asyncpg.create_pool(
        dsn=settings.database_url,       
        min_size=2,                      
        max_size=10,                     
        command_timeout=60,              
    )


async def disconnect_db() -> None:
    global _pool
    if _pool:
        await _pool.close()
        _pool = None


def get_pool() -> asyncpg.Pool:
    if _pool is None:
        raise RuntimeError("Database pool is not initialized. Was connect_db() called?")
    return _pool


async def init_schema() -> None:
    pool = get_pool()
    async with pool.acquire() as conn:   
        
        await conn.execute("""
            -- Enable the pgvector extension so we can store vector(3072) columns
            -- IF NOT EXISTS = safe to re-run, won't error if already enabled
            CREATE EXTENSION IF NOT EXISTS vector;

            -- documents: one row per uploaded PDF or TXT file
            CREATE TABLE IF NOT EXISTS documents (
                id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                -- gen_random_uuid() = Postgres generates the UUID, no app code needed
                name         TEXT NOT NULL,
                file_type    TEXT NOT NULL,        -- 'pdf' or 'txt'
                size_bytes   INTEGER,
                uploaded_at  TIMESTAMPTZ DEFAULT now(),
                chunk_count  INTEGER DEFAULT 0,
                status       TEXT DEFAULT 'processing'
                -- 'processing' → 'indexed' → 'error'
            );

            -- chunks: one row per piece of content extracted from a document
            -- could be a text block, a markdown table, or an image caption
            CREATE TABLE IF NOT EXISTS chunks (
                id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                doc_id       UUID REFERENCES documents(id) ON DELETE CASCADE,
                -- ON DELETE CASCADE: delete the document → all its chunks auto-delete
                content      TEXT NOT NULL,
                chunk_index  INTEGER,              -- position within the document
                page_num     INTEGER,
                chunk_type   TEXT DEFAULT 'text',  -- 'text' | 'table' | 'image_caption'
                metadata     JSONB DEFAULT '{}'    -- flexible extra fields (section header, bbox, etc)
            );

            -- embeddings: one row per chunk, stores the 1536-dim vector
            -- separated from chunks so we can JOIN only when doing vector search
            CREATE TABLE IF NOT EXISTS embeddings (
                id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                chunk_id     UUID REFERENCES chunks(id) ON DELETE CASCADE,
                embedding    vector(1536)
                -- vector(1536) is the pgvector type — stores text-embedding-3-large output truncated to 1536
            );

            -- HNSW index: makes cosine similarity search O(log n) instead of O(n)
            -- m=16: graph connectivity (higher = better recall, more memory)
            -- ef_construction=64: index build quality (higher = slower build, better recall)
            CREATE INDEX IF NOT EXISTS embeddings_hnsw_idx
                ON embeddings USING hnsw (embedding vector_cosine_ops)
                WITH (m = 16, ef_construction = 64);

            -- query_cache: stores results of previous queries to skip the pipeline
            -- TTL is enforced in app logic (we check created_at + cache_ttl_seconds)
            CREATE TABLE IF NOT EXISTS query_cache (
                query_hash   TEXT PRIMARY KEY,     -- SHA256 of the query string
                query_text   TEXT,
                result       JSONB,                -- the full pipeline result as JSON
                created_at   TIMESTAMPTZ DEFAULT now()
            );
        """)
