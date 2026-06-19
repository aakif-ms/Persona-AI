import asyncio
from connectors.gmail import get_gmail_service, check_new_emails
from connectors.calendar import get_calendar_service, check_new_events
from queue.redis_queue import push_event

async def observation_loop():
    print("Initializing Obervation Layer")

    gmail_service = get_gmail_service()
    calendar_service = get_calendar_service()
    
    print("Sensors Active. Monitoring...")

    while True:
        try:
            new_mails = await check_new_emails(gmail_service)
            for email in new_mails:
                await push_event(email)
                print(f"Queued Email: {email.get('message_id')}")

            new_events = await check_new_events(calendar_service)
            for event in new_events:
                await push_event(event)
                print(f"Queued Event: {event.get('title')}")
        except Exception as e:
            print(f"Observation Error: {e}")
        
        await asyncio.sleep(20)

if __name__ == "__main__":
    asyncio.run(observation_loop())