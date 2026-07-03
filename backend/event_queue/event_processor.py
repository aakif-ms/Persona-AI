import asyncio
import os
import sys

BACKEND_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if BACKEND_ROOT not in sys.path:
    sys.path.insert(0, BACKEND_ROOT)

from connectors.gmail import get_gmail_service, check_new_emails
from connectors.calendar import get_calendar_service, check_new_events
from event_queue.redis_queue import push_event

async def observation_loop(max_cycles=5):
    print("Initializing Observation Layer")

    gmail_service = get_gmail_service()
    calendar_service = get_calendar_service()

    print("Sensors Active. Monitoring...")

    cycle = 0

    while cycle < max_cycles:
        try:
            print(f"Cycle {cycle + 1}")

            new_mails = await check_new_emails(gmail_service)
            for email in new_mails:
                await push_event(email)

            new_events = await check_new_events(calendar_service)
            for event in new_events:
                await push_event(event)

        except Exception as e:
            print(f"Observation Error: {e}")

        cycle += 1
        await asyncio.sleep(20)

    print("Observer stopped")

if __name__ == "__main__":
    asyncio.run(observation_loop())