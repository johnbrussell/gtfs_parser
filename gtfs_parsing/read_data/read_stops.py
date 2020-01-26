import csv
import os

from gtfs_parsing.data_structures.data_structures import stopLocation
from gtfs_parsing.read_data.csv_reading_helper_functions import separate_columns_from_data


def read_stop_locations(agency, date, data_location):
    # Reads "trips.txt" file, returns dict(trip_id: routeInfo).
    #  routeInfo is defined in data_structures.py
    with open(os.path.join(data_location, agency, 'data', date, 'stops.txt')) as f:
        unformatted_stop_locations = csv.reader(f, delimiter=',')
        stop_location_namedtuple = separate_columns_from_data(unformatted_stop_locations)
        stop_location_dict = create_stop_location_dict(stop_location_namedtuple)
    return stop_location_dict


def create_stop_location_dict(stop_location_namedtuple):
    data = stop_location_namedtuple.data
    cols = stop_location_namedtuple.columns

    return {stop[cols['stop_id']]: stopLocation(lat=float(stop[cols['stop_lat']].strip()),
                                                long=float(stop[cols['stop_lon']].strip())) for stop in data}
