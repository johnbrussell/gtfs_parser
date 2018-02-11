import csv
import os
from global_defaults import DATA_SET, tripInfo, stopDeparture, routeInfo
from gtfs_parsing.csv_reading_helper_functions import separate_columns_from_data, coerce_integer_to_string


def read_stop_times(trip_type_dict):
    # Reads "stop_times.txt file"
    #  Returns dict(trip_id: tripInfo(tripStops=dict(stop_sequence: stopDeparture), tripType=route_id)).
    #  tripInfo is defined in global_defaults.py.
    with open(os.path.join('./data', DATA_SET, 'stop_times.txt')) as f:
        unformatted_stop_times = csv.reader(f, delimiter=',')
        stop_times_namedtuple = separate_columns_from_data(unformatted_stop_times)
        trip_dict = create_trip_type_stop_time_dict(stop_times_namedtuple, trip_type_dict)
    return trip_dict


def create_trip_type_stop_time_dict(input_namedtuple, trip_types):
    # Converts input data into dict(trip_id: tripInfo) format.  tripInfo is defined in global_defaults.py.
    stop_times_rows = input_namedtuple.data
    stop_time_cols = input_namedtuple.columns

    trip_stop_time_dict = to_trip_stop_time_dict(stop_times_rows, stop_time_cols)

    return add_trip_type_to_trip_stop_times_dict(trip_stop_time_dict, trip_types)


def to_trip_stop_time_dict(stop_times, stop_cols):
    # Returns nested dictionaries: dict(trip_id: dict(stop_sequence: stopDeparture))
    #  stopDeparture namedtuple is defined in global_defaults.py
    trip_dict = dict()

    for stop in stop_times:
        trip_id = stop[stop_cols['trip_id']]
        stop_seq = coerce_integer_to_string(stop[stop_cols['stop_sequence']])

        if trip_id not in trip_dict:
            trip_dict[trip_id] = dict()

        trip_dict[trip_id][stop_seq] = stopDeparture(
            stopId=stop[stop_cols['stop_id']], departureTime=stop[stop_cols['departure_time']])

    return trip_dict


def add_trip_type_to_trip_stop_times_dict(trips_dict, trip_type_dict):
    # Takes trips_dict of format dict(trip_id: dict(stop_sequence: stopDeparture))
    #  Returns dict(trip_id: tripInfo(tripStops=dict(stop_sequence: stopDeparture), tripType=routeInfo)).
    #  tripInfo and stopDeparture are defined in global_defaults.py.
    for trip_id in trips_dict:
        trips_dict[trip_id] = tripInfo(
            tripStops=trips_dict[trip_id], tripRouteInfo=trip_type_dict.get(trip_id, routeInfo('UNKNOWN', 'UNKNOWN')))
    return trips_dict
