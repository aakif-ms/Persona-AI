from fastapi import BackgroundTasks, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from event_queue.redis_queue import push_event
from memory.episodic_memory import get_recent_events
from memory.semantic_memory import SemanticMemory

app = FastAPI(title="Persona AI - Backend API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EventPayload(BaseModel):
    event_type: str
    source: str
    data: dict

@app.post("/webhook/event")
async def receive_event(event: EventPayload, background_task: BackgroundTasks):
    background_task.add_task(push_event, event.model_dump())
    return {"status": "Event queued successfully"}

@app.get("/api/events")
async def api_get_event():
    events = await get_recent_events(limit=10)
    return {"events": events}

@app.get("/api/memory/semantic")
async def api_get_semantic_memory():
    semantic_mem = SemanticMemory()
    relationships = await semantic_mem.get_all_relationships()
    await semantic_mem.close()
    return {"relationships": relationships}

@app.get("/api/agents/status")
async def api_get_agent_status():
    return {
        "agents": [
            {"name": "Research Agent", "status": "Waiting"},
            {"name": "Scheduler Agent", "status": "Waiting"},
            {"name": "Reminder Agent", "status": "Waiting"}
        ]
    }