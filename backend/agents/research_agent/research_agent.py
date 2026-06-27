import os 
from tavily import TavilyClient
from memory.episodic_memory import store_event

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

async def execute_research(instruction: str, payload: str):
    query = payload.get("query", instruction)
    print(f"Research Agent searching for: {query}")

    response = tavily_client.search(query=query, search_depth="basic")

    results = response.get("results", [])
    summary = "\n".join([f"- {r['title']}: {r['content'][:150]}..." for r in results[:3]])

    await store_event(
        event_type="research_completed",
        description=f"Reseach on '{query}' completed",
        metadata={"qeury": query, "findings": summary}
    )
    
    print(f"Research completed and saved to memory. \nFindings:\n{summary}")
    return summary