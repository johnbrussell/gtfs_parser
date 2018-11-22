import csv
import unittest

from gtfs_parsing.data_structures.data_structures import stopDeparture, routeInfo, tripInfo
from gtfs_parsing.read_data.csv_reading_helper_functions import separate_columns_from_data
from gtfs_parsing.read_data.read_stop_times import to_trip_stop_time_dict, add_trip_type_to_trip_stop_times_dict
from gtfs_parsing.read_data.read_routes import create_route_type_dict
from gtfs_parsing.read_data.read_trips import create_trip_type_dict


class TestReadData(unittest.TestCase):
    @staticmethod
    def readTestFile(file_path):
        unformatted_data = csv.reader(file_path, delimiter=',')
        return separate_columns_from_data(unformatted_data)

    def testTripStopTimeDict(self):
        trip_stop_time_dict_expected = {
            'Logan-22-Weekday-trip': {
                '1': stopDeparture(stopId='Logan-Subway', departureTime='08:00:00'),
                '2': stopDeparture(stopId='Logan-RentalCarCenter', departureTime='08:04:00')
            },
            'Logan-22-Weekend-trip': {
                '1': stopDeparture(stopId='Logan-Subway', departureTime='12:00:00'),
                '2': stopDeparture(stopId='Logan-RentalCarCenter', departureTime='12:04:00'),
                '7': stopDeparture(stopId='Logan-A', departureTime='12:26:00')
            },
            'Logan-33-Weekday-trip': {
                '1': stopDeparture(stopId='Logan-Subway', departureTime='08:00:00'),
                '2': stopDeparture(stopId='Logan-RentalCarCenter', departureTime='08:04:00')
            },
            'Logan-33-Weekend-trip': {
                '1': stopDeparture(stopId='Logan-Subway', departureTime='12:00:00'),
                '2': stopDeparture(stopId='Logan-RentalCarCenter', departureTime='12:04:00'),
            },
            'Logan-55-Weekday-trip': {
                '1': stopDeparture(stopId='Logan-Subway', departureTime='00:00:00'),
                '2': stopDeparture(stopId='Logan-RentalCarCenter', departureTime='00:04:00')
            },
            'Logan-55-Weekend-trip': {
                '1': stopDeparture(stopId='Logan-Subway', departureTime='00:00:00'),
                '2': stopDeparture(stopId='Logan-RentalCarCenter', departureTime='00:04:00')
            },
            'Logan-66-Weekday-trip': {
                '1': stopDeparture(stopId='Logan-Dock', departureTime='06:00:00'),
                '3': stopDeparture(stopId='Logan-B', departureTime='06:07:00')
            },
            'Logan-66-Weekend-trip': {
                '1': stopDeparture(stopId='Logan-Dock', departureTime='07:00:00'),
                '2': stopDeparture(stopId='Logan-A', departureTime='07:05:00')
            },
            'CR-Saturday-Fall-17-1752': {
                '1': stopDeparture(stopId='Readville', departureTime='7:30:00'),
                '2': stopDeparture(stopId='Fairmount', departureTime='7:33:00')
            }
        }

        with open('./gtfs_parsing/tests/test_csv_files/test_stop_times.txt') as f:
            input_namedtuple = self.readTestFile(f)
            trip_stop_time_dict_actual = to_trip_stop_time_dict(input_namedtuple.data, input_namedtuple.columns)

        for key in trip_stop_time_dict_expected:
            self.assertIn(key, trip_stop_time_dict_actual)
        for key in trip_stop_time_dict_actual:
            self.assertIn(key, trip_stop_time_dict_expected)

        for key in trip_stop_time_dict_expected:
            for nested_key in trip_stop_time_dict_expected[key]:
                self.assertIn(nested_key, trip_stop_time_dict_actual[key])
        for key in trip_stop_time_dict_actual:
            for nested_key in trip_stop_time_dict_actual[key]:
                self.assertIn(nested_key, trip_stop_time_dict_expected[key])

        for key in trip_stop_time_dict_expected:
            for nested_key in trip_stop_time_dict_expected[key]:
                self.assertEqual(trip_stop_time_dict_expected[key][nested_key],
                                 trip_stop_time_dict_actual[key][nested_key])

    def testRouteTypeDict(self):
        route_type_dict_expected = {
            'CapeFlyer':    '2',
            'Logan-22':     '3',
            'Logan-33':     '3',
            'Logan-55':     '3',
            'Logan-66':     '3',
            'CR-Fairmount': '2'
        }

        with open('./gtfs_parsing/tests/test_csv_files/test_routes.txt') as f:
            input_namedtuple = self.readTestFile(f)
            route_type_dict_actual = create_route_type_dict(input_namedtuple)

        for key in route_type_dict_expected:
            self.assertIn(key, route_type_dict_actual)
        for key in route_type_dict_actual:
            self.assertIn(key, route_type_dict_expected)
            self.assertEqual(route_type_dict_expected[key], route_type_dict_actual[key])

    def testTripTypeDict(self):
        trip_type_dict_expected = {
            'Logan-22-Weekday-trip':    routeInfo(routeId='Logan-22', routeType='3'),
            'Logan-22-Weekend-trip':    routeInfo(routeId='Logan-22', routeType='3'),
            'Logan-33-Weekday-trip':    routeInfo(routeId='Logan-33', routeType='3'),
            'Logan-33-Weekend-trip':    routeInfo(routeId='Logan-33', routeType='3'),
            'Logan-55-Weekday-trip':    routeInfo(routeId='Logan-55', routeType='3'),
            'Logan-55-Weekend-trip':    routeInfo(routeId='Logan-55', routeType='3'),
            'Logan-66-Weekday-trip':    routeInfo(routeId='Logan-66', routeType='3'),
            'Logan-66-Weekend-trip':    routeInfo(routeId='Logan-66', routeType='3'),
            'CR-Saturday-Fall-17-1752': routeInfo(routeId='CR-Fairmount', routeType='2')
        }

        with open('./gtfs_parsing/tests/test_csv_files/test_trips.txt') as f:
            with open('./gtfs_parsing/tests/test_csv_files/test_routes.txt') as g:
                input_namedtuple = self.readTestFile(f)
                trip_type_dict_actual = create_trip_type_dict(
                    input_namedtuple, create_route_type_dict(self.readTestFile(g)))

        for key in trip_type_dict_expected:
            self.assertIn(key, trip_type_dict_actual)
        for key in trip_type_dict_actual:
            self.assertIn(key, trip_type_dict_expected)
            self.assertEqual(trip_type_dict_expected[key], trip_type_dict_actual[key])

    def testTripTypeStopTimeDict(self):
        trip_type_stop_time_dict_expected = {
            'Logan-22-Weekday-trip': tripInfo(
                tripStops={
                    '1': stopDeparture(stopId='Logan-Subway', departureTime='08:00:00'),
                    '2': stopDeparture(stopId='Logan-RentalCarCenter', departureTime='08:04:00')},
                tripRouteInfo=routeInfo(routeId='Logan-22', routeType='3')
            ),
            'CR-Saturday-Fall-17-1752': tripInfo(
                tripStops={
                    '1': stopDeparture(stopId='Readville', departureTime='7:30:00'),
                    '2': stopDeparture(stopId='Fairmount', departureTime='7:33:00')},
                tripRouteInfo=routeInfo(routeId='CR-Fairmount', routeType='2')
            )
        }

        trip_stop_time_dict_given = {
            'Logan-22-Weekday-trip': {
                '1': stopDeparture(stopId='Logan-Subway', departureTime='08:00:00'),
                '2': stopDeparture(stopId='Logan-RentalCarCenter', departureTime='08:04:00')
            },
            'CR-Saturday-Fall-17-1752': {
                '1': stopDeparture(stopId='Readville', departureTime='7:30:00'),
                '2': stopDeparture(stopId='Fairmount', departureTime='7:33:00')
            }
        }

        with open('./gtfs_parsing/tests/test_csv_files/test_trips.txt') as g:
            with open('./gtfs_parsing/tests/test_csv_files/test_routes.txt') as h:
                trip_type_stop_time_dict_actual = add_trip_type_to_trip_stop_times_dict(
                    trip_stop_time_dict_given, create_trip_type_dict(
                        self.readTestFile(g), create_route_type_dict(self.readTestFile(h))))

        for key in trip_type_stop_time_dict_expected:
            self.assertIn(key, trip_type_stop_time_dict_actual)
        for key in trip_type_stop_time_dict_actual:
            self.assertIn(key, trip_type_stop_time_dict_expected)

            self.assertEqual(trip_type_stop_time_dict_expected[key].tripRouteInfo,
                             trip_type_stop_time_dict_actual[key].tripRouteInfo)

            for nested_key in trip_type_stop_time_dict_expected[key].tripStops:
                self.assertIn(nested_key, trip_type_stop_time_dict_actual[key].tripStops)
            for nested_key in trip_type_stop_time_dict_actual[key].tripStops:
                self.assertIn(nested_key, trip_type_stop_time_dict_expected[key].tripStops)
