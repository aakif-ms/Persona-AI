from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from event_queue.redis_queue import push_event

app = FastAPI(title="Persona AI - Observation Layer")

class EventPayload(BaseModel):
    event_type: str
    source: str
    data: dict

@app.get("/")
async def health_check():
    return {"status": "Observation Layer Active"}

@app.post("/webhook/event")
async def receive_event(event: EventPayload, background_task: BackgroundTasks):
    background_task.add_task(push_event, event.model_dump())
    return {"status": "Event queued successfully"}