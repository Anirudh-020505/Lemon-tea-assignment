import asyncio
from app.database import connect_db, disconnect_db, get_pool

async def main():
    await connect_db()
    pool = get_pool()
    async with pool.acquire() as conn:
        await conn.execute("DELETE FROM documents")
        print("Deleted all documents")
    await disconnect_db()

if __name__ == "__main__":
    asyncio.run(main())
