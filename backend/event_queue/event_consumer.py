import asyncio
import os
import sys

BACKEND_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if BACKEND_ROOT not in sys.path:
    sys.path.insert(0, BACKEND_ROOT)

from event_queue.redis_queue import pop_event
from memory.episodic_memory import store_event, init_db
from memory.semantic_memory import SemanticMemory

async def consume_events():
    print("Initializing Episodic Database...")
    await init_db()
    
    print("Initializing Semantic Graph Database...")
    semantic_mem = SemanticMemory()
    
    print("Database Systems Ready. Listening for events...")

    while True:
        event = await pop_event()
        if event:
            event_type = event.get('event_type', 'unknown')
            
            if event_type == "email_received":
                desc = f"Received email snippet: {event.get('snippet', '')[:75]}..."
                
                if "interview" in event.get('snippet', '').lower() or "scheduled" in event.get('snippet', '').lower():
                    await semantic_mem.create_user_relationship("User", "APPLYING_TO", "Google")
                    await semantic_mem.create_user_relationship("User", "WEAK_AT", "DSA")  

            elif event_type == "calendar_event_detected":
                desc = f"Scheduled event: {event.get('title')} starting at {event.get('start_time')}"
                if "google" in event.get('title', '').lower():
                    await semantic_mem.create_user_relationship("User", "INTERVIEWING_WITH", "Google")
            else:
                desc = "Unknown event detected."

            await store_event(event_type=event_type, description=desc, metadata=event)
            print(f"Successfully processed and updated semantic maps for: {event_type}")
        else:
            await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(consume_events())