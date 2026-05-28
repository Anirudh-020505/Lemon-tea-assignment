from contextlib import asynccontextmanager  
 
from fastapi import FastAPI                
from fastapi.middleware.cors import CORSMiddleware  

from app.config import get_settings       
from app.database import connect_db, disconnect_db, init_schema 

 
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 DocMind starting up...")
    
    await connect_db()       
    
    await init_schema()      
    
    print(" Database connected and schema ready")
    
    yield  
 
    print("DocMind shutting down...")
    await disconnect_db()    
 
 
app = FastAPI(
    title="DocMind API",                    
    description="Multi-Document Enterprise RAG Assistant",
    version="1.0.0",
    lifespan=lifespan,                      
    docs_url="/docs",                       
    redoc_url="/redoc",                     
)
 
 
settings = get_settings()
 
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,  
    
    allow_credentials=True,   
    
    allow_methods=["*"],      
    
    allow_headers=["*"],      
)
 
 
 
from app.routes import upload, documents, query
app.include_router(upload.router, prefix="/api")
app.include_router(documents.router, prefix="/api")
app.include_router(query.router, prefix="/api")
 
 
@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "docmind-api"}
 
 
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",      
        host="0.0.0.0",  
        port=8000,        
        reload=True,      
    )