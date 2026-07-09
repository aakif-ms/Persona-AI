import asyncio
import os
import sys

BACKEND_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if BACKEND_ROOT not in sys.path:
    sys.path.insert(0, BACKEND_ROOT)

import asyncio
from event_queue.redis_queue import pop_event, push_task
from memory.episodic_memory import store_event, init_db
from memory.semantic_memory import SemanticMemory
from memory.long_term_memory import init_qdrant, search_similar_memories
from services.summarizer import trigger_summarization_job
from agents.planner_agent.planner import planner_app
from agents.task_decomposer.decomposer import decompose_goal

SUMMARY_BATCH_SIZE = 5


async def consume_events(max_cycles=None):
    print("Initializing Databases...")
    db_ready = await init_db()
    if not db_ready:
        print("Database is unavailable; continuing without persistence.")
    try:
        await init_qdrant()
    except Exception as exc:
        print(f"Qdrant unavailable: {exc}")
    semantic_mem = SemanticMemory()
    summary_batch = []
    print("Systems Ready. Listening for events...")

    cycle = 0

    try:
        while max_cycles is None or cycle < max_cycles:
            event = await pop_event()
            if event:
                event_type = event.get('event_type', 'unknown')
                source = event.get('source', 'unknown_source')
                desc = f"Raw Event: {event_type}"

                await store_event(event_type=event_type, description=desc, metadata=event)

                await semantic_mem.create_user_relationship(source, "OBSERVED", f"event:{event_type}")

                summary_batch.append({"event_type": event_type, "description": desc})
                if len(summary_batch) >= SUMMARY_BATCH_SIZE:
                    await trigger_summarization_job(summary_batch)
                    summary_batch.clear()

                past_context = await search_similar_memories(str(event), limit= 2)

                initial_state = {
                    "event": event,
                    "memory_context": past_context,
                    "action_required": False,
                    "goal": None,
                    "reasoning": ""
                }

                final_state = planner_app.invoke(initial_state)

                if final_state["action_required"]:
                    goal = final_state['goal']
                    print(f"Goal Generated: {goal}")

                    await semantic_mem.create_user_relationship(source, "NEEDS", goal)

                    tasks = decompose_goal(goal, event)

                    for task in tasks:
                        await push_task(task)
                        print(f"Queued Task for {task['agent'].upper()} Agent: {task['instruction']}")

                cycle += 1
            else:
                cycle += 1
                await asyncio.sleep(1)
    finally:
        if summary_batch:
            await trigger_summarization_job(summary_batch)
        await semantic_mem.close()

if __name__ == "__main__":
    print("Reached main")
    asyncio.run(consume_events())
    print("All Tasks analyzed")