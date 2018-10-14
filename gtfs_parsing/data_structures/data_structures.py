from collections import namedtuple


runConfiguration = namedtuple('agencyDateInfo', ['agency', 'date'])
dataWithColumns = namedtuple('dataWithColumns', ['data', 'columns'])
stopDeparture = namedtuple('stopDeparture', ['stopId', 'departureTime'])
tripInfo = namedtuple('tripInfo', ['tripStops', 'tripRouteInfo'])
routeInfo = namedtuple('routeInfo', ['routeId', 'routeType'])
