import asyncio
from app.database import connect_db, disconnect_db
from app.retrieval.dense import DenseRetriever
from app.retrieval.sparse import SparseRetriever
import traceback

async def main():
    await connect_db()
    
    query = "experience"
    
    print("Testing DenseRetriever...")
    try:
        dense_results = await DenseRetriever.retrieve(query)
        print(f"Dense found {len(dense_results)} chunks")
    except Exception as e:
        print("DenseRetriever failed:")
        traceback.print_exc()

    print("Testing SparseRetriever...")
    try:
        sparse_results = await SparseRetriever.retrieve(query)
        print(f"Sparse found {len(sparse_results)} chunks")
    except Exception as e:
        print("SparseRetriever failed:")
        traceback.print_exc()
        
    await disconnect_db()

if __name__ == "__main__":
    asyncio.run(main())
