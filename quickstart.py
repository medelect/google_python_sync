from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json

# SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'cs3.json'
# APPLICATION_NAME = 'Google Calendar API Python Quickstart2'
APPLICATION_NAME = '777'


def get_credentials():
    """Gets valid user credentials from storage.
       If nothing has been stored, or if the stored credentials are invalid,
       the OAuth2 flow is completed to obtain the new credentials.

       Returns:
       Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
    'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

# def send_event():
#     credentials1 = get_credentials()
#     http1 = credentials1.authorize(httplib2.Http())
#     service1 = discovery.build('calendar', 'v3', http=http1)



def main():
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """



    gte, ste , id, lst = [0,1,0,0]

    print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  SEND EVENT   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
    if ste:

        # Refer to the Python quickstart on how to setup the environment:
        # https://developers.google.com/google-apps/calendar/quickstart/python
        # Change the scope to 'https://www.googleapis.com/auth/calendar' and delete any
        # stored credentials.
        event = {
            'summary': 'TotalHedMessage',
            'location': 'myPlace',
            'description': 'SomeActions',
            'start': {
                'dateTime': '2017-03-03T09:30:00-02:00',
                'timeZone': 'Europe/Kiev',
            },
            'end': {
                'dateTime': '2017-03-03T20:00:00-02:00',
                'timeZone': 'Europe/Kiev',
            },
            'recurrence': [
                'RRULE:FREQ=DAILY;COUNT=1'
            ],
            'attendees': [
                {'email': 'lpage@example.com'},
                {'email': 'sbrin@example.com'},
            ],
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
                ],
            },
        }


        credentials = get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)


        # myCalendarId = 'plumb_callendar'
        myCalendarId = 'primary'
        event = service.events().insert(calendarId=myCalendarId, body=event).execute()
        print('Event created: %s' % (event.get('htmlLink')))

    print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  EVENT LIST   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
    if gte:
        credentials = get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)

        now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        eventsResult = service.events().list(
                calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
                orderBy='startTime').execute()
        events = eventsResult.get('items', [])


        if not events:
            print('No upcoming events found.')
        for event in events:

            # start = event['start'].get('dateTime', event['start'].get('date'))
            # print(start, event['summary'])
            print('--------------------------------------------------------------------')
            for e in event: print(e, '  -->', event[e])


        # for e in dir(events[0]): print(e)
        # print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        # for e in events[0]: print(e ,'  -->' , events[0][e])
    print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ CALENDAR LIST @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
    if lst:
        page_token = None
        while True:
            calendar_list = service.calendarList().list(pageToken=page_token).execute()
            for calendar_list_entry in calendar_list['items']:
                print
                calendar_list_entry['summary']
            page_token = calendar_list.get('nextPageToken')
            if not page_token:
                print ('111111111111111111')
                break
    print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ CALENDAR ID   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
    if id:
        calendar_list_entry = service.calendarList().get(calendarId='fcqesms2rprp8hdka7u89ihigs@group.calendar.google.com').execute()
        print(calendar_list_entry['summary'])







if __name__ == '__main__':
    main()
