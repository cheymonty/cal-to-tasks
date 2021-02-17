from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/tasks']


def main():
    calendar_id = input("Enter calendar ID of Google Calendar you would like to move to Tasks: ")

    creds = None
  
    if os.path.exists('tokenCal.pickle'):
        with open('tokenCal.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentialsCal.json', SCOPES[0])
            creds = flow.run_local_server(port=0)
        
        with open('tokenCal.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Gets all future events from this calendar')
    events_result = service.events().list(calendarId=calendar_id, timeMin=now,
                                        singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    # prints out calendar events
    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

    if len(events) == 0:
        print("There are no calendar events to move to Tasks")
    else:
        cal_to_tasks(events)



def cal_to_tasks(events):
    creds = None

    if os.path.exists('tokenTask.pickle'):
        with open('tokenTask.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentialsTask.json', SCOPES[1])
            creds = flow.run_local_server(port=0)
       
        with open('tokenTask.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('tasks', 'v1', credentials=creds)

    
    results = service.tasklists().list(maxResults=10).execute()
    task_lists = results.get('items', [])

    for event in events: 
        title = event['summary']
        description = ""
        if "description" in event:
            description = event['description']
    
        due = event['start'].get('dateTime')
        if due == None:
            due = event['start'].get('date') + "T09:00:00-05:00"
      
        request_body = {
            'title': title,
            'notes': description,
            'due': due,
            'deleted': False,
            'status': 'needsAction'
        }

        r = service.tasks().insert(
            tasklist=task_lists[0]['id'],
            body=request_body
        ).execute()

    print("Created " + str(len(events)) + " new tasks")

if __name__ == '__main__':
    main()