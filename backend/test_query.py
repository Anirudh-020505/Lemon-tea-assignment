import asyncio
import json
from app.database import connect_db, disconnect_db
from app.pipeline.graph import app_graph
from app.pipeline.state import GraphState

async def main():
    await connect_db()
    
    initial_state = GraphState(
        query="What is Anirudh's experience?",
        original_query="What is Anirudh's experience?",
        loop_count=0,
        generation="",
        context_sufficient=False,
        documents=[]
    )
    
    def on_token(token):
        print(f"Token: {token}", end="", flush=True)
        
    config = {
        "configurable": {
            "token_callback": on_token
        }
    }
    
    try:
        async for event in app_graph.astream(initial_state, config=config):
            for node_name, state_update in event.items():
                print(f"\n--- Node: {node_name} ---")
                if "documents" in state_update:
                    print(f"Found {len(state_update['documents'])} documents")
                if "final_context" in state_update:
                    print(f"Final context len: {len(state_update['final_context'])}")
                if "context_sufficient" in state_update:
                    print(f"Context sufficient: {state_update['context_sufficient']}")
                if "generation" in state_update:
                    print(f"Generation output len: {len(state_update['generation'])}")
    except Exception as e:
        print(f"\n\nERROR: {e}")
        
    await disconnect_db()

if __name__ == "__main__":
    asyncio.run(main())
