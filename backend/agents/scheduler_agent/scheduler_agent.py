from connectors.calendar import get_calendar_service

async def execute_scheduling(instruction: str, payload: dict):
    print(f"Scheduler Agent processing: {instruction}")

    service = get_calendar_service()
    
    title = payload.get("title", "Autonomous Prep Session")
    start_time = payload.get("start_time")
    end_time = payload.get("end_time")

    if not start_time or not end_time:
        print("Scheduler Error: Missing start or end time.")
        return 
    
    event = {
        'summary': title,
        'description': instruction,
        'start': {
            'datetime': start_time,
            'timezone': 'UTC',
        },
        'end': {
            'datetime': end_time,
            'timezone': 'UTC',    
        },
    }
    
    created_event = service.events().insert(calendarId='primary', body=event).execute()
    print(f"Event created: {created_event.get('htmlLink')}")
    return created_event