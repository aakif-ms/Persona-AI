import asyncio
import json
import redis.asyncio as redis
from agents.research_agent.research_agent import execute_research
from agents.scheduler_agent.scheduler_agent import execute_scheduling
from agents.reminder_agent.reminder_agent import execute_reminder

redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
TASK_QUEUE_NAME = "persona_task_queue"

async def process_task(task: dict):
    """Routes the task to the specialized agent."""
    agent_type = task.get("agent")
    instruction = task.get("instruction", "")
    payload = task.get("payload", {})
    
    try:
        if agent_type == "research":
            await execute_research(instruction, payload)
        elif agent_type == "scheduler":
            await execute_scheduling(instruction, payload)
        elif agent_type == "reminder":
            await execute_reminder(instruction, payload)
        else:
            print(f"Unknown agent type requested: {agent_type}")
    except Exception as e:
        print(f"Error executing task for {agent_type}: {str(e)}")

async def task_worker_loop():
    """Continuously monitors the task queue for new agent instructions."""
    print("Specialized Agents Online. Waiting for tasks...")
    
    while True:
        task_data = await redis_client.blpop(TASK_QUEUE_NAME, timeout=1)
        if task_data:
            task = json.loads(task_data[1])
            print(f"\n--- New Task Received ---")
            print(f"Routing to: {task.get('agent').upper()} AGENT")
            await process_task(task)
        else:
            await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(task_worker_loop())