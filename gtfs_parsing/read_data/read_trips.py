import csv
import os

from gtfs_parsing.data_structures.data_structures import routeInfo, tripInfo
from gtfs_parsing.read_data.csv_reading_helper_functions import separate_columns_from_data


def read_trip_types(agency, date, route_type_dict, data_location):
    # Reads "trips.txt" file, returns dict(trip_id: routeInfo).
    #  routeInfo is defined in data_structures.py
    with open(os.path.join(data_location, agency, 'data', date, 'trips.txt')) as f:
        unformatted_trip_times = csv.reader(f, delimiter=',')
        trip_types_namedtuple = separate_columns_from_data(unformatted_trip_times)
        trip_type_dict = create_trip_type_dict(trip_types_namedtuple, route_type_dict)
    return trip_type_dict


def create_trip_type_dict(trip_type_namedtuple, route_type_dict):
    trip_type_dict = dict()
    trip_data = trip_type_namedtuple.data
    trip_cols = trip_type_namedtuple.columns

    for trip in trip_data:
        route_type = route_type_dict[trip[trip_cols['route_id']]]
        trip_type_dict[trip[trip_cols['trip_id']]] = tripInfo(
            tripStops=list(),
            tripRouteInfo=routeInfo(routeId=trip[trip_cols['route_id']], routeType=route_type),
            serviceId=trip[trip_cols['service_id']]
        )

    return trip_type_dict
