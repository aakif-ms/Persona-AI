import redis.asyncio as redis
import json

redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

QUEUE_NAME = "persona_event_queue"
TASK_QUEUE_NAME = "persona_task_queue"

async def push_event(event_data: dict):
    await redis_client.lpush(QUEUE_NAME, json.dumps(event_data))

async def pop_event():
    event = await redis_client.brpop(QUEUE_NAME)
    if event:
        return json.loads(event[1])
    return None


async def push_task(task_data: dict):
    await redis_client.rpush(TASK_QUEUE_NAME, json.dumps(task_data))

async def pop_task():
    task = await redis_client.blpop(TASK_QUEUE_NAME, timeout=1)
    if task:
        return json.loads(task[1])
    return None