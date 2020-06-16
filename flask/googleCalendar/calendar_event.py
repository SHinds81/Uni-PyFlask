from __future__ import print_function
from googleapiclient.discovery import build
#from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools


class GoogleCalendar:
    def __init__(self):
        'empty'
        
        
    def creatEvent(self, location, carId, brand, bodyType, color, numSeats, hrCost, startTime, endTime):
        """
        create a google claendar even for person booking the car

        :type location: string
        :param location: holds a booked cars pickup location

        :type carId: string
        :param carId: contains a booked cars id

        :type brand: string
        :param brand: contains booked cars brand

        :type bodyType: string
        :param bodyType: contains booked cars body type

        :type color: string
        :param color: booked cars color

        :type numSeats: string
        :param numSeats: booked cars number of seats

        :type hrCost: string
        :param hrCost: booked cars cost per hour

        :type startTime: string
        :param startTime: booked cars start date

        :type endTime: string
        :param endTime: booked cars end date
        """
        try:
            import argparse
            flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
        except ImportError:
            flags = None

        #AIzaSyAPMjOInB-1AY6kmCT39UAOP1tQUCN1dKs

        SCOPES = 'https://www.googleapis.com/auth/calendar'
        store = file.Storage('storage.json')
        creds = store.get()

        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
            creds = tools.run_flow(flow, store, flags) \
                    if flags else tools.run(flow, store)

        #if flags:
        #        creds = tools.run_flow(flow, store, flags)
        #    else:
        #        creds = tools.run(flow, store)
                
        CAL = build('calendar', 'v3', http=creds.authorize(Http()))

        GMT_OFF = '+10:00' #east australian time

        event = "car hire" + str(carId)
        description = ("Car ID: " + str(carId) + ", " +
                       "Brand: "+ brand + ", " +
                       "Body Type: " + bodyType + ", " +
                       "Color: " + color + ", " +
                       "Number of Seats: " + numSeats + ", " +
                       "Cost per Hour" + hrCost)


        EVENT = {'summary': event, 'location': location, 'description': description,
                 'start': {'dateTime': '%s%s' % (startTime, GMT_OFF)}, 'end': {'dateTime': '%s%s' % (endTime, GMT_OFF)}}

        #        EVENT = {'summary': 'event', 'location': '800 Howard St., San Francisco, CA 94103', 'description': 'A event description',
        #                 'start': {'dateTime': '2020-05-15T10:00:00%s' % GMT_OFF}, 'end': {'dateTime': '2020-05-15T11:00:00%s' % GMT_OFF},}


        e = CAL.events().insert(calendarId='primary', sendNotifications=True, body=EVENT).execute()

        print('''*** %r event added: Start: %s End: %s''' % (e['summary'].encode('utf-8'), e['start']['dateTime'], e['end']['dateTime']))
    
if __name__ == "__main__":
    c = GoogleCalendar()
    c.creatEvent('location', 1, 'brand', 'bodyType', 'color', 'numSeats', 'hrCost', '2020-05-27T11:00:00', '2020-05-27T12:00:00')
