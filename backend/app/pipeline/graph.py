from langgraph.graph import StateGraph, END
from app.pipeline.state import GraphState
from app.pipeline.nodes import (
    classify_node,
    expand_node,
    retrieve_node,
    fuse_node,
    rerank_node,
    diversity_node,
    self_check_node,
    generate_node,
    score_node,
    cache_node
)

workflow = StateGraph(GraphState)

workflow.add_node("classify", classify_node)
workflow.add_node("expand", expand_node)
workflow.add_node("retrieve", retrieve_node)
workflow.add_node("fuse", fuse_node)
workflow.add_node("rerank", rerank_node)
workflow.add_node("diversity", diversity_node)
workflow.add_node("self_check", self_check_node)
workflow.add_node("generate", generate_node)
workflow.add_node("score", score_node)
workflow.add_node("cache", cache_node)

def route_after_self_check(state: GraphState) -> str:
    if state.get("context_sufficient") or state.get("loop_count", 0) >= 1:
        return "generate"
    return "retrieve" 

workflow.set_entry_point("classify")

workflow.add_edge("classify", "expand")
workflow.add_edge("expand", "retrieve")
workflow.add_edge("retrieve", "fuse")
workflow.add_edge("fuse", "rerank")
workflow.add_edge("rerank", "diversity")
workflow.add_edge("diversity", "self_check")

workflow.add_conditional_edges(
    "self_check",
    route_after_self_check,
    {
        "generate": "generate",
        "retrieve": "retrieve"
    }
)

workflow.add_edge("generate", "score")
workflow.add_edge("score", "cache")
workflow.add_edge("cache", END)

app_graph = workflow.compile()