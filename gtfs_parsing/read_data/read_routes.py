import csv
import os

from gtfs_parsing.read_data.csv_reading_helper_functions import separate_columns_from_data, coerce_integer_to_string


def read_routes(agency, date):
    # Reads "routes.txt" file, returns dict(route_id: route_type)
    with open(os.path.join('./agencies', agency, 'data', date, 'routes.txt')) as f:
        unformatted_trip_times = csv.reader(f, delimiter=',')
        route_types_namedtuple = separate_columns_from_data(unformatted_trip_times)
        return create_route_type_dict(route_types_namedtuple)


def create_route_type_dict(routes_namedtuple):
    route_type_dict = dict()
    routes_data = routes_namedtuple.data
    routes_cols = routes_namedtuple.columns

    for route in routes_data:
        route_type_dict[route[routes_cols['route_id']]] = coerce_integer_to_string(route[routes_cols['route_type']])

    return route_type_dict
