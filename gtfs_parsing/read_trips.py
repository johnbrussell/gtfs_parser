import csv
import os

from global_defaults import DATA_SET, ROUTE_TYPE_DESCRIPTION_DICT, routeInfo
from gtfs_parsing.csv_reading_helper_functions import separate_columns_from_data


def read_trip_types(route_type_dict):
    # Reads "trips.txt" file, returns dict(trip_id: routeInfo).
    #  routeInfo is defined in global_defaults.py
    with open(os.path.join('./data', DATA_SET, 'trips.txt')) as f:
        unformatted_trip_times = csv.reader(f, delimiter=',')
        trip_types_namedtuple = separate_columns_from_data(unformatted_trip_times)
        return create_trip_type_dict(trip_types_namedtuple, route_type_dict)


def create_trip_type_dict(trip_type_namedtuple, route_type_dict):
    trip_type_dict = dict()
    trip_data = trip_type_namedtuple.data
    trip_cols = trip_type_namedtuple.columns

    for trip in trip_data:
        route_type = get_route_type(trip[trip_cols['route_id']], route_type_dict)
        trip_type_dict[trip[trip_cols['trip_id']]] = routeInfo(routeId=trip[trip_cols['route_id']],
                                                               routeType=route_type)

    return trip_type_dict


def get_route_type(route_id, route_type_dict):
    return ROUTE_TYPE_DESCRIPTION_DICT.get(route_type_dict[route_id], 'UNKNOWN')
