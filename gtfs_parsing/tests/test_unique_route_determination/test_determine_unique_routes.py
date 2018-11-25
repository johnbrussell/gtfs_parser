import unittest

from gtfs_parsing.unique_route_determination import determine_unique_routes
from gtfs_parsing.data_structures.data_structures import routeInfo, stopDeparture, tripInfo, uniqueRouteInfo


class TestDetermineUniqueRoutes(unittest.TestCase):
    TEST_TRIP_DICT = {
        't1': tripInfo(
            tripStops={
                '1': stopDeparture(stopId='s2', departureTime='12:00'),
                '2': stopDeparture(stopId='s3', departureTime='12:01'),
                '3': stopDeparture(stopId='s4', departureTime='12:02')
            },
            tripRouteInfo=routeInfo(routeId="testId", routeType="Plane"),
            serviceId='service'
        ),
        't2': tripInfo(
            tripStops={
                '1': stopDeparture(stopId='s2', departureTime='12:00'),
                '2': stopDeparture(stopId='s3', departureTime='12:01'),
                '3': stopDeparture(stopId='s4', departureTime='12:02')
            },
            tripRouteInfo=routeInfo(routeId="differentTestId", routeType="Bus"),
            serviceId='service'
        ),
        't3': tripInfo(
            tripStops={
                '1': stopDeparture(stopId='s2', departureTime='12:00'),
                '2': stopDeparture(stopId='s3', departureTime='12:01')
            },
            tripRouteInfo=routeInfo(routeId="testId", routeType="Plane"),
            serviceId='service'
        ),
        't4': tripInfo(
            tripStops={
                '1': stopDeparture(stopId='s2', departureTime='12:00'),
                '2': stopDeparture(stopId='s3', departureTime='12:01'),
                '3': stopDeparture(stopId='s4', departureTime='12:02')
            },
            tripRouteInfo=routeInfo(routeId="testId", routeType="Plane"),
            serviceId='service'
        ),
        't5': tripInfo(
            tripStops={
                '1': stopDeparture(stopId='s1', departureTime='11:59'),
                '2': stopDeparture(stopId='s2', departureTime='12:00'),
                '3': stopDeparture(stopId='s3', departureTime='12:01'),
                '4': stopDeparture(stopId='s4', departureTime='12:02')
            },
            tripRouteInfo=routeInfo(routeId="testId", routeType="Plane"),
            serviceId='service'
        )
    }

    def test_is_list_of_identical_tuples(self):
        test_list_of_idential_stop_ids = [("id1", "id1"), ("2id", "2id"), ("i3d", "i3d")]
        test_list_of_non_idential_stop_ids = [("id1", "id1"), ("2id", "4id"), ("i3d", "i3d")]

        self.assertTrue(determine_unique_routes.is_list_of_identical_tuples(test_list_of_idential_stop_ids))
        self.assertFalse(determine_unique_routes.is_list_of_identical_tuples(test_list_of_non_idential_stop_ids))

    def test_get_trip_stops(self):
        expected_trip_stops = ['s2', 's3', 's4']
        actual_trip_stops = determine_unique_routes.get_trip_stops(self.TEST_TRIP_DICT, 't1')

        self.assertTrue(determine_unique_routes.is_list_of_identical_tuples(zip(expected_trip_stops,
                                                                                actual_trip_stops)))

    def test_add_unique_route(self):
        expected_output = {1: uniqueRouteInfo(tripIds=list(), routeInfo=routeInfo(routeId="testId", routeType="Plane"))}

        actual_dict = dict()
        test_route_id = 1
        test_route_info = routeInfo(routeId="testId", routeType="Plane")

        determine_unique_routes.add_unique_route(actual_dict, test_route_id, test_route_info)

        self.assertEqual(tuple(expected_output.keys()), tuple(actual_dict.keys()))

        for key in expected_output:
            self.assertTrue(len(expected_output[key].tripIds) == len(actual_dict[key].tripIds))
            self.assertTrue(expected_output[key].routeInfo == actual_dict[key].routeInfo)

    def test_place_trip_into_unique_routes_dict(self):
        expected_output = {1: uniqueRouteInfo(tripIds=['t1'], routeInfo=routeInfo(routeId="testId", routeType="Plane"))}

        actual_dict = {1: uniqueRouteInfo(tripIds=list(), routeInfo=routeInfo(routeId="testId", routeType="Plane"))}
        test_new_route_id = 1
        test_new_trip_id = 't1'

        determine_unique_routes.place_trip_into_unique_routes_dict(actual_dict, test_new_route_id, test_new_trip_id)

        self.assertEqual(tuple(expected_output.keys()), tuple(actual_dict.keys()))

        for key in expected_output:
            self.assertTrue(determine_unique_routes.is_list_of_identical_tuples(zip(expected_output[key].tripIds,
                                                                                    actual_dict[key].tripIds)))

    def test_all_stops_match(self):
        test_route_id = 1
        test_route_dict = {1: uniqueRouteInfo(tripIds=['t1'], routeInfo=routeInfo(routeId="testId", routeType="Plane"))}

        self.assertTrue(determine_unique_routes.all_stops_match('t2', test_route_id, self.TEST_TRIP_DICT,
                                                                test_route_dict))
        self.assertFalse(determine_unique_routes.all_stops_match('t3', test_route_id, self.TEST_TRIP_DICT,
                                                                 test_route_dict))
        self.assertTrue(determine_unique_routes.all_stops_match('t4', test_route_id, self.TEST_TRIP_DICT,
                                                                test_route_dict))
        self.assertFalse(determine_unique_routes.all_stops_match('t5', test_route_id, self.TEST_TRIP_DICT,
                                                                 test_route_dict))

    def test_identify_known_route(self):
        test_route_dict = {1: uniqueRouteInfo(tripIds=['t1'], routeInfo=routeInfo(routeId="testId", routeType="Plane"))}

        expected_unknown_route = (False, 2)
        expected_known_route = (True, 1)

        self.assertEqual(expected_unknown_route, determine_unique_routes.identify_known_route(
            test_route_dict, determine_unique_routes.get_trip_route_info('t2', self.TEST_TRIP_DICT), 't2',
            self.TEST_TRIP_DICT
        ))
        self.assertEqual(expected_unknown_route, determine_unique_routes.identify_known_route(
            test_route_dict, determine_unique_routes.get_trip_route_info('t3', self.TEST_TRIP_DICT), 't3',
            self.TEST_TRIP_DICT
        ))
        self.assertEqual(expected_known_route, determine_unique_routes.identify_known_route(
            test_route_dict, determine_unique_routes.get_trip_route_info('t4', self.TEST_TRIP_DICT), 't4',
            self.TEST_TRIP_DICT
        ))

    def test_to_unique_route_trip_dict(self):
        test_date_trip_dict = {
            1: {'t1', 't2', 't3', 't4', 't5'}
        }

        expected_route_dict = {
            1: uniqueRouteInfo(tripIds=['t1', 't4'], routeInfo=routeInfo(routeId="testId", routeType="Plane")),
            2: uniqueRouteInfo(tripIds=['t2'], routeInfo=routeInfo(routeId="differentTestId", routeType="Bus")),
            3: uniqueRouteInfo(tripIds=['t3'], routeInfo=routeInfo(routeId="testId", routeType="Plane")),
            4: uniqueRouteInfo(tripIds=['t5'], routeInfo=routeInfo(routeId="testId", routeType="Plane"))
        }

        actual_route_dict = determine_unique_routes.to_unique_route_trip_dict(self.TEST_TRIP_DICT, test_date_trip_dict)

        self.assertEqual(tuple(expected_route_dict.keys()), tuple(actual_route_dict.keys()))

        for key in expected_route_dict:
            self.assertEqual(tuple(expected_route_dict[key].tripIds), tuple(actual_route_dict[key].tripIds))
            self.assertEqual(expected_route_dict[key].routeInfo, actual_route_dict[key].routeInfo)

    def test_trips_operating_within_analysis_dates(self):
        expected_output = {'t1', 't2', 't3'}

        test_input = {
            1: {'t1', 't2', 't3'}
        }

        actual_output = set(determine_unique_routes.trips_operating_within_analysis_dates(test_input))

        self.assertTrue(expected_output.issubset(actual_output))
        self.assertTrue(actual_output.issubset(expected_output))
