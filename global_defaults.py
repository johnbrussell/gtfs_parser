from collections import namedtuple


DATA_SET = 'MBTA_feb_10_2018'
dataWithColumns = namedtuple('dataWithColumns', ['data', 'columns'])
stopDeparture = namedtuple('stopDeparture', ['stopId', 'departureTime'])
tripInfo = namedtuple('tripInfo', ['tripStops', 'tripRouteInfo'])
routeInfo = namedtuple('routeInfo', ['routeId', 'routeType'])

ROUTE_TYPE_DESCRIPTION_DICT = {
    '0':    'Light Rail',
    '1':    'Subway',
    '2':    'Rail',
    '3':    'Bus',
    '4':    'Ferry',
    '5':    'Cable Car',
    '6':    'Gondola',
    '7':    'Funicular',
    'WALK': 'Walk'
}
