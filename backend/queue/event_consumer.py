import asyncio
from queue.redis_queue import pop_event
from memory.episodic_memory import store_event, init_db

async def consume_events():
    print("Initializing Episodic Database...")
    await init_db()
    print("Database Ready. Listening for events on Redis Queue")

    while True:
        event = await pop_event()
        if event:
            event_type = event.get('event_type', 'unknown')

            if event_type == "email_received":
                desc = f"Received email snippet: {event.get('snippet', '')[:75]}..."
            elif event_type == "calendar_event_detected":
                desc = f"Scheduled event: {event.get('title')} starting at {event.get('start_time')}"
            else:
                desc = "Unknown event detected."
            
            print(f"Consuming Event: {event_type} -> Archiving to PostgreSQL")

            await store_event(event_type=event_type, description=desc, metadata=event)
        else:
            await asyncio.sleep(1)
    
if __name__ == "__main__":
    asyncio.run(consume_events)