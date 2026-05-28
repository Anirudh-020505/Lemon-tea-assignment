import json
import asyncio
from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse

from app.pipeline.graph import app_graph

router = APIRouter()

@router.get("/query")
async def query_endpoint(
    question: str = Query(..., description="The search query question")
):
    
    async def sse_generator():
        yield f"data: {json.dumps({'event': 'cache_hit', 'data': False})}\n\n"

        queue = asyncio.Queue()
        loop = asyncio.get_running_loop()

        def token_callback(token: str):
            loop.call_soon_threadsafe(queue.put_nowait, {"event": "token", "data": token})

        initial_state = {
            "query": question,
            "original_query": question,
            "raw_chunks": [],
            "fused_chunks": [],
            "reranked_chunks": [],
            "final_context": [],
            "context_sufficient": False,
            "generation": "",
            "confidence_score": 0,
            "citations_verified": False,
            "loop_count": 0,
            "trace": []
        }

        config = {
            "configurable": {
                "token_callback": token_callback
            }
        }

        async def run_graph():
            try:
                async for event in app_graph.astream(initial_state, config=config):
                    if not event:
                        continue
                    
                    node_name = list(event.keys())[0]
                    state_update = event[node_name]
                    
                    details = f"Completed {node_name}."
                    if node_name == "classify" and "reasoning_effort" in state_update:
                        details = f"Analyzed query. Reasoning effort set to {state_update['reasoning_effort'].upper()}."
                    elif node_name == "expand" and "expanded_queries" in state_update:
                        details = f"Generated {len(state_update['expanded_queries']) - 1} alternative query variants for deeper recall."
                    elif node_name == "retrieve" and "raw_chunks" in state_update:
                        details = f"Retrieved {len(state_update['raw_chunks'])} raw chunks from dense and sparse vector indices."
                    elif node_name == "fuse" and "fused_chunks" in state_update:
                        details = f"Applied Reciprocal Rank Fusion to extract top {len(state_update['fused_chunks'])} chunks."
                    elif node_name == "rerank" and "reranked_chunks" in state_update:
                        details = f"Reranked top {len(state_update['reranked_chunks'])} chunks using FlashRank cross-encoder."
                    elif node_name == "diversity" and "final_context" in state_update:
                        details = f"Filtered context to {len(state_update['final_context'])} highly diverse, non-redundant chunks."
                    elif node_name == "self_check" and "context_sufficient" in state_update:
                        details = f"Verified context sufficiency: {'PASSED' if state_update['context_sufficient'] else 'FAILED'}. Loop count: {state_update.get('loop_count', 1)}."
                    elif node_name == "generate":
                        details = f"Generated final grounded answer using LLM."
                    elif node_name == "score" and "confidence_score" in state_update:
                        details = f"Evaluated answer. Confidence: {state_update['confidence_score']}/100. Citations verified: {state_update.get('citations_verified', False)}."
                        await queue.put({"event": "score", "data": {"confidence": state_update["confidence_score"], "citations": state_update.get("citations_verified", False)}})
                    elif node_name == "cache":
                        details = f"Saved successful generation to semantic cache."
                    
                    trace_msg = {"step": node_name.capitalize(), "status": "completed", "message": details}
                    await queue.put({"event": "trace", "data": trace_msg})
                    
                    if node_name == "diversity" and "final_context" in state_update:
                        final_docs = state_update["final_context"]
                        ui_docs = []
                        for idx, doc in enumerate(final_docs):
                            ui_docs.append({
                                "id": idx,
                                "document": doc.get("metadata", {}).get("filename", "Unknown"),
                                "score": round(doc.get("score", 0.0), 3),
                                "content": doc.get("content", "")
                            })
                        await queue.put({"event": "docs", "data": ui_docs})
                        
                await queue.put({"event": "done", "data": "done"})
            except Exception as e:
                print(f"Graph execution failed: {e}")
                await queue.put({"event": "error", "data": str(e)})
            finally:
                await queue.put(None)

        bg_task = asyncio.create_task(run_graph())

        while True:
            item = await queue.get()
            if item is None:
                break
            yield f"data: {json.dumps(item)}\n\n"
            
        await bg_task

    return StreamingResponse(sse_generator(), media_type="text/event-stream")
