import datetime
import datefinder
import pickle
import os.path
import json
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def authenticate():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists('static/schedule/credentials/iot_token.pickle'):
        with open('static/schedule/credentials/iot_token.pickle', 'rb') as token:
            creds = pickle.load(token)
            
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('static/schedule/credentials/client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('static/schedule/credentials/iot_token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    return creds


def get_list_of_events(service, calendar_id, today):
    page_token = None
    # today = datetime.date.today().strftime('%Y-%m-%d')
    start_time = '{}T00:00:00+08:00'.format(today)
    end_time = '{}T23:59:59+08:00'.format(today)

    while True:
        events = service.events().list(calendarId=calendar_id, pageToken=page_token, timeMin=start_time, timeMax=end_time).execute()
        # print(json.dumps(events, indent=4))
        # for event in events['items']:
        #     # print(event['id'])
        #     print(json.dumps(event, indent=4))
        page_token = events.get('nextPageToken')
        if not page_token:
            break
    
    return events["items"]