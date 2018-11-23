from collections import namedtuple


runConfiguration = namedtuple('agencyDateInfo', ['agency', 'date', 'start_date', 'end_date', 'route_types'])
dataWithColumns = namedtuple('dataWithColumns', ['data', 'columns'])
stopDeparture = namedtuple('stopDeparture', ['stopId', 'departureTime'])
tripInfo = namedtuple('tripInfo', ['tripStops', 'tripRouteInfo'])
routeInfo = namedtuple('routeInfo', ['routeId', 'routeType'])
uniqueRouteInfo = namedtuple('uniqueRouteInfo', ['tripIds', 'routeInfo'])

# Want stop -> outbound route -> time -> travel time dict.
