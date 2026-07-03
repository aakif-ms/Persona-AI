import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/calendar.readonly'
]

def get_calendar_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('calendar', 'v3', credentials=creds)

async def check_new_events(service):
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    events_result = service.events().list(
        calendarId='primary', timeMin=now,
        maxResults=5, singleEvents=True,
        orderBy='startTime'
    ).execute()
    
    events = events_result.get('items', [])
    system_events = []

    for event in events:
        start = event['start'].get('datetime', event['start'].get('date'))
        system_events.append({
            "event_type": "calendar_event_detected",
            "title": event.get('summary', 'Untitled Event'),
            "start_time": start,
            "creator": event.get('creator', {}).get('email', 'Unknown')
        })
    
    return system_events