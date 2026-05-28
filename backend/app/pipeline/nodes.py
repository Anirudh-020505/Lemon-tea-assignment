import re
import json
import asyncio
from typing import Dict, Any, List
from openai import AsyncOpenAI
from langchain_core.runnables import RunnableConfig

from app.config import get_settings
from app.pipeline.state import GraphState, DocumentChunk
from app.retrieval.dense import DenseRetriever
from app.retrieval.sparse import SparseRetriever
from app.retrieval.reranker import FlashRankReranker

settings = get_settings()
openai_client = AsyncOpenAI(api_key=settings.openai_api_key, base_url=settings.openai_base_url)

async def classify_node(state: GraphState) -> Dict[str, Any]:
    query = state.get("query", "").lower()
    
    complex_words = r"\b(compare|contrast|analyze|difference|evaluate|synthesize)\b"
    if re.search(complex_words, query):
        effort = "high"
    elif len(query.split()) > 10:
        effort = "medium"
    else:
        effort = "low"
        
    return {"reasoning_effort": effort, "loop_count": state.get("loop_count", 0)}

async def expand_node(state: GraphState) -> Dict[str, Any]:
    query = state.get("query")
    
    prompt = f"Generate 3 variations of this search query to improve retrieval recall. Return ONLY a JSON list of 3 strings. Query: '{query}'"
    
    try:
        response = await openai_client.chat.completions.create(
            model=settings.llm_model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        content = response.choices[0].message.content
        try:
            data = json.loads(content)
            if isinstance(data, dict):
                variants = next(iter(data.values()))
            else:
                variants = data
            if not isinstance(variants, list):
                variants = []
        except:
            variants = []
    except Exception:
        variants = []
        
    return {"expanded_queries": [query] + variants[:3]}

async def retrieve_node(state: GraphState) -> Dict[str, Any]:
    queries = state.get("expanded_queries", [state.get("query")])
    
    all_chunks = []
    
    tasks = []
    for q in queries:
        tasks.append(DenseRetriever.retrieve(q, top_k=10))
        tasks.append(SparseRetriever.retrieve(q, top_k=10))
        
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    for res in results:
        if isinstance(res, list):
            all_chunks.extend(res)
        else:
            print(f"Retrieval Exception: {res}")
            
    unique_chunks = {}
    for chunk in all_chunks:
        if chunk["id"] not in unique_chunks:
            unique_chunks[chunk["id"]] = chunk
            
    return {"raw_chunks": list(unique_chunks.values())}

async def fuse_node(state: GraphState) -> Dict[str, Any]:
    raw_chunks = state.get("raw_chunks", [])
    if not raw_chunks:
        return {"fused_chunks": []}
        
    raw_chunks.sort(key=lambda x: x["score"], reverse=True)
    
    k = 60
    rrf_scores = {}
    
    for rank, chunk in enumerate(raw_chunks):
        cid = chunk["id"]
        if cid not in rrf_scores:
            rrf_scores[cid] = 0.0
        rrf_scores[cid] += 1.0 / (k + rank + 1)
        
    for chunk in raw_chunks:
        chunk["score"] = rrf_scores[chunk["id"]]
        
    raw_chunks.sort(key=lambda x: x["score"], reverse=True)
    
    return {"fused_chunks": raw_chunks[:20]} 

async def rerank_node(state: GraphState) -> Dict[str, Any]:
    query = state.get("query")
    fused_chunks = state.get("fused_chunks", [])
    
    if not fused_chunks:
        return {"reranked_chunks": []}
        
    try:
        reranked = FlashRankReranker.rerank(query, fused_chunks, top_k=6)
    except Exception as e:
        print(f"Reranking failed: {e}")
        reranked = fused_chunks[:6]
        
    return {"reranked_chunks": reranked}

async def diversity_node(state: GraphState) -> Dict[str, Any]:
    reranked = state.get("reranked_chunks", [])
    if not reranked:
        return {"final_context": []}
        
    def jaccard_similarity(t1: str, t2: str) -> float:
        set1 = set(t1.lower().split())
        set2 = set(t2.lower().split())
        if not set1 or not set2: return 0.0
        return len(set1.intersection(set2)) / len(set1.union(set2))
        
    final_context = []
    for chunk in reranked:
        is_duplicate = False
        for kept_chunk in final_context:
            if jaccard_similarity(chunk["content"], kept_chunk["content"]) > 0.8:
                is_duplicate = True
                break
        if not is_duplicate:
            final_context.append(chunk)
            
    return {"final_context": final_context}

async def self_check_node(state: GraphState) -> Dict[str, Any]:
    query = state.get("query")
    context = state.get("final_context", [])
    loop_count = state.get("loop_count", 0)
    
    if not context:
        return {"context_sufficient": False, "loop_count": loop_count + 1}
        
    context_text = "\n\n".join([c["content"] for c in context])
    prompt = f"Does the following context contain enough information to answer the question? Answer ONLY 'YES' or 'NO'.\n\nQuestion: {query}\n\nContext: {context_text}"
    
    try:
        response = await openai_client.chat.completions.create(
            model=settings.llm_model,
            messages=[{"role": "user", "content": prompt}]
        )
        answer = response.choices[0].message.content.strip().upper()
        sufficient = "YES" in answer
    except:
        sufficient = True 
        
    return {"context_sufficient": sufficient, "loop_count": loop_count + 1}

async def generate_node(state: GraphState, config: RunnableConfig) -> Dict[str, Any]:
    query = state.get("query")
    context = state.get("final_context", [])
    
    configurable = config.get("configurable", {})
    token_callback = configurable.get("token_callback")

    if not context:
        msg = "I couldn't find any relevant information in the documents to answer your question."
        if token_callback:
            token_callback(msg)
        return {"generation": msg}
        
    context_blocks = []
    for idx, doc in enumerate(context):
        context_blocks.append(f"Source [{idx+1}]: {doc.get('metadata', {}).get('filename', 'Unknown')} (Page {doc['page_number']})\nContent: {doc['content']}")
    context_str = "\n\n".join(context_blocks)
    
    prompt = (
        f"You are DocMind. Answer the question using ONLY the provided context. "
        f"Always cite your sources using bracketed numbers like [1], [2].\n\n"
        f"Question: {query}\n\nContext:\n{context_str}"
    )
    
    try:
        response = await openai_client.chat.completions.create(
            model=settings.llm_model,
            messages=[{"role": "user", "content": prompt}],
            stream=True
        )
        
        full_response = []
        async for chunk in response:
            if chunk.choices and chunk.choices[0].delta.content:
                token = chunk.choices[0].delta.content
                full_response.append(token)
                if token_callback:
                    token_callback(token)
                    
        return {"generation": "".join(full_response)}
    except Exception as e:
        print(f"Generation failed: {e}")
        err_msg = "Error generating response from the model."
        if token_callback:
            token_callback(err_msg)
        return {"generation": err_msg}

async def score_node(state: GraphState) -> Dict[str, Any]:
    generation = state.get("generation", "")
    
    citations = re.findall(r'\[\d+\]', generation)
    citations_verified = len(citations) > 0
    
    return {"confidence_score": 95 if citations_verified else 70, "citations_verified": citations_verified}

async def cache_node(state: GraphState) -> Dict[str, Any]:
    return state
