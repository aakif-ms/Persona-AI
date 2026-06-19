import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_gmail_service():
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
    
    return build('gmail', 'v1', credentials=creds)

async def check_new_emails(service):
    results = service.users().messages().list(userId='me', labelIds=['Inbox'], maxResults=5).execute()
    messages = results.get('messages', [])
    
    events = []
    for msg in messages:
        txt = service.users().messages().get(userId='me', id=msg['id']).execute()
        events.append({
            "event_type": "email_received",
            "message_id": msg['id'],
            "snippet": txt['snippet']
        })
    return events