import datetime
from memory.long_term_memory import store_memory_summary

async def trigger_summarization_job(events_batch: list):
    if not events_batch:
        return

    summary_text = "Recent Activity Summary: " + " | ".join(
        [f"{e.get('event_type')}: {e.get('description')}" for e in events_batch]
    )
    
    metadata = {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "event_count": len(events_batch)
    }

    await store_memory_summary(summary_text, metadata)
    print(f"Stored long-term memory embedding: {summary_text[:50]}...")