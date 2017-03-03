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

def get_credentials(scopes, app_name, auth_file, conn_file_name):
    #home_dir = os.path.expanduser('~')
    home_dir = './'
    credential_dir = os.path.join(home_dir, '.connectors')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, conn_file_name)

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(auth_file, scopes)
        flow.user_agent = app_name
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def get_goo_event():
    SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
    CLIENT_SECRET_FILE = 'cl_sic_get.json'
    APPLICATION_NAME = 'test_get_e'

    credentials = get_credentials(SCOPES, APPLICATION_NAME, CLIENT_SECRET_FILE, 'get_goo_key.json' )
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    eventsResult = service.events().list(
        calendarId='primary', timeMin=now, maxResults=33, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])
    return events

def set_goo_event(event):
    SCOPES = 'https://www.googleapis.com/auth/calendar'
    CLIENT_SECRET_FILE = 'cl_sic_set.json'
    APPLICATION_NAME = 'test_set_e'

    credentials = get_credentials(SCOPES, APPLICATION_NAME, CLIENT_SECRET_FILE, 'set_goo_key.json' )
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    event = service.events().insert(calendarId='primary', body=event).execute()
    return event.get('htmlLink')

def del_goo_event():
    SCOPES = 'https://www.googleapis.com/auth/calendar'
    CLIENT_SECRET_FILE = 'cl_sic_set.json'
    APPLICATION_NAME = 'test_set_e'

    credentials = get_credentials(SCOPES, APPLICATION_NAME, CLIENT_SECRET_FILE, 'set_goo_key.json' )
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    service.events().delete(calendarId='primary', eventId='jcnmg2jtbas2i8mdadhnpb190s_20170301T113000Z').execute()
    # return event.get('htmlLink')

def upd_goo_event(event):
    SCOPES = 'https://www.googleapis.com/auth/calendar'
    CLIENT_SECRET_FILE = 'cl_sic_set.json'
    APPLICATION_NAME = 'test_set_e'

    credentials = get_credentials(SCOPES, APPLICATION_NAME, CLIENT_SECRET_FILE, 'set_goo_key.json' )
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    updated_event = service.events().update(calendarId='primary', eventId='2gu2ke0jr9muao4fth28o1o93g', body=event).execute()
    return updated_event['updated']

def upd_goo_event_light():
    SCOPES = 'https://www.googleapis.com/auth/calendar'
    CLIENT_SECRET_FILE = 'cl_sic_set.json'
    APPLICATION_NAME = 'test_set_e'

    credentials = get_credentials(SCOPES, APPLICATION_NAME, CLIENT_SECRET_FILE, 'set_goo_key.json' )
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    event = service.events().get(calendarId='primary', eventId='2gu2ke0jr9muao4fth28o1o93g').execute()

    event['summary'] = 'YAY AY DONE IT!!!'

    updated_event = service.events().update(calendarId='primary', eventId=event['id'], body=event).execute()

    print(updated_event['updated'])

def get_list_goo_calendars(event):
    pass
    # page_token = None
    # while True:
    #     calendar_list = service.calendarList().list(pageToken=page_token).execute()
    #     for calendar_list_entry in calendar_list['items']:
    #         print
    #         calendar_list_entry['summary']
    #         page_token = calendar_list.get('nextPageToken')
    #         if not page_token:
    #             print ('111111111111111111')
    #             break

def get_id_goo_calendar():
    pass
    # calendar_list_entry = service.calendarList().get(calendarId='fcqesms2rprp8hdka7u89ihigs@group.calendar.google.com').execute()
    # print(calendar_list_entry['summary'])



def main():
    event_list = get_goo_event()
    if not event_list:
        print('No upcoming events found.')
    for event in event_list:
        print('--------------------------------------------------------------------')
        for e in event: print(e, '  -->', event[e])
    print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
    eve = {
        'summary': '1YAYdddddddddddddddddddddddddddddd',
        'location': 'myPlace',
        'description': 'SomeActions',
        'start': {
            'dateTime': '2017-03-20T09:30:00-02:00',
            'timeZone': 'Europe/Kiev',
        },
        'end': {
            'dateTime': '2017-03-20T20:00:00-02:00',
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
    # print(set_goo_event(eve))
    # print(del_goo_event())
    # print(upd_goo_event(eve))
    print(upd_goo_event_light())

if __name__ == '__main__':
    main()


 #   WSGIPythonPath /var/www/dwpp/dwppp:/var/www/dwpp/.env/lib/python2.7/site-packages