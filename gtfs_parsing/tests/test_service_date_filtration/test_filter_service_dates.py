import unittest
from datetime import datetime

from gtfs_parsing.service_date_filtration.filter_service_dates import to_date_trip_dict, \
    date_outside_of_service_range, add_trip_if_no_exception, add_trip_if_valid_day_of_week
from gtfs_parsing.service_date_filtration import date_helpers
from gtfs_parsing.data_structures.data_structures import routeInfo, serviceDates, stopDeparture, tripInfo


class TestReadData(unittest.TestCase):
    TEST_SERVICE_EXCEPTIONS_DICT = {
        's2': {
            datetime(2018, 11, 22): False,
            datetime(2018, 11, 12): True
        }
    }
    TEST_SERVICE_DATES_DICT = {
        's1': serviceDates(
            start_date=datetime(year=2018, month=11, day=11),
            end_date=datetime(year=2018, month=11, day=25),
            serviceDays={
                'm': True,
                't': False,
                'w': True,
                'r': False,
                'f': True,
                's': False,
                'u': True
            }
        ),
        's2': serviceDates(
            start_date=datetime(year=2018, month=11, day=11),
            end_date=datetime(year=2018, month=11, day=23),
            serviceDays={
                'm': False,
                't': True,
                'w': False,
                'r': True,
                'f': False,
                's': True,
                'u': False
            }
        )
    }
    TEST_TRIP_DICT = {
        't1': tripInfo(
            tripStops={
                '1': stopDeparture(stopId='s1', departureTime='12:00'),
                '2': stopDeparture(stopId='s2', departureTime='12:01'),
                '3': stopDeparture(stopId='s3', departureTime='12:02')
            },
            tripRouteInfo=routeInfo(routeId="testId", routeType="Plane"),
            serviceId='s1'
        ),
        't2': tripInfo(
            tripStops={
                '1': stopDeparture(stopId='s1', departureTime='12:00'),
                '2': stopDeparture(stopId='s2', departureTime='12:01'),
                '3': stopDeparture(stopId='s3', departureTime='12:02')
            },
            tripRouteInfo=routeInfo(routeId="differentTestId", routeType="Bus"),
            serviceId='s1'
        ),
        't3': tripInfo(
            tripStops={
                '1': stopDeparture(stopId='s2', departureTime='12:00'),
                '2': stopDeparture(stopId='s3', departureTime='12:01')
            },
            tripRouteInfo=routeInfo(routeId="testId", routeType="Plane"),
            serviceId='s2'
        )
    }

    def test_to_date_trip_dict(self):
        expected_date_trip_dict = {
            datetime(year=2018, month=11, day=11): {'t1', 't2'},
            datetime(year=2018, month=11, day=12): {'t1', 't2', 't3'},
            datetime(year=2018, month=11, day=13): {'t3'},
            datetime(year=2018, month=11, day=14): {'t1', 't2'},
            datetime(year=2018, month=11, day=15): {'t3'},
            datetime(year=2018, month=11, day=16): {'t1', 't2'},
            datetime(year=2018, month=11, day=17): {'t3'},
            datetime(year=2018, month=11, day=18): {'t1', 't2'},
            datetime(year=2018, month=11, day=19): {'t1', 't2'},
            datetime(year=2018, month=11, day=20): {'t3'},
            datetime(year=2018, month=11, day=21): {'t1', 't2'},
            datetime(year=2018, month=11, day=22): set(),
            datetime(year=2018, month=11, day=23): {'t1', 't2'},
            datetime(year=2018, month=11, day=24): set(),
            datetime(year=2018, month=11, day=25): {'t1', 't2'}
        }

        actual_date_trip_dict = to_date_trip_dict(self.TEST_TRIP_DICT, '2018-11-11', '2018-11-25',
                                                  self.TEST_SERVICE_DATES_DICT, self.TEST_SERVICE_EXCEPTIONS_DICT)

        self.assertEqual(tuple(expected_date_trip_dict.keys()), tuple(actual_date_trip_dict.keys()))

        for key in expected_date_trip_dict:
            self.assertTrue(expected_date_trip_dict[key].issubset(actual_date_trip_dict[key]))
            self.assertTrue(actual_date_trip_dict[key].issubset(expected_date_trip_dict[key]))

    def test_date_outside_of_service_range(self):
        nov1 = datetime(year=2018, month=11, day=1)
        nov3 = datetime(year=2018, month=11, day=3)
        nov5 = datetime(year=2018, month=11, day=5)

        # Arguments are: (current date, start date, service end date, service start date, end date)
        self.assertFalse(date_outside_of_service_range(nov3, nov1, nov5, nov1, nov5))
        self.assertFalse(date_outside_of_service_range(nov3, nov3, nov5, nov1, nov5))
        self.assertFalse(date_outside_of_service_range(nov3, nov1, nov5, nov3, nov5))
        self.assertFalse(date_outside_of_service_range(nov3, nov1, nov5, nov1, nov3))
        self.assertFalse(date_outside_of_service_range(nov3, nov1, nov3, nov1, nov5))
        self.assertTrue(date_outside_of_service_range(nov3, nov1, nov5, nov5, nov5))
        self.assertTrue(date_outside_of_service_range(nov3, nov1, nov1, nov1, nov5))
        self.assertTrue(date_outside_of_service_range(nov5, nov5, nov1, nov5, nov5))
        self.assertTrue(date_outside_of_service_range(nov5, nov5, nov5, nov5, nov1))

    def test_add_trip_if_no_exception(self):
        valid_trips_dict = {
            datetime(year=2018, month=11, day=12): set(),
            datetime(year=2018, month=11, day=13): set(),
            datetime(year=2018, month=11, day=14): set(),
            datetime(year=2018, month=11, day=22): set(),
        }

        def wrap_add_trip_if_no_exception(current_date, trp, svc_id):
            add_trip_if_no_exception(self.TEST_SERVICE_EXCEPTIONS_DICT, svc_id, current_date,
                                     self.TEST_SERVICE_DATES_DICT[svc_id].serviceDays,
                                     date_helpers.to_day_of_week(current_date.weekday()), valid_trips_dict,
                                     trp)

        expected_date_trip_dict = {
            datetime(year=2018, month=11, day=12): {'t3'},
            datetime(year=2018, month=11, day=13): {'t3'},
            datetime(year=2018, month=11, day=14): set(),
            datetime(year=2018, month=11, day=22): set(),
        }

        for trip in self.TEST_TRIP_DICT:
            service_id = self.TEST_TRIP_DICT[trip].serviceId
            if service_id != 's2':
                continue
            wrap_add_trip_if_no_exception(datetime(year=2018, month=11, day=12), trip, service_id)
            wrap_add_trip_if_no_exception(datetime(year=2018, month=11, day=13), trip, service_id)
            wrap_add_trip_if_no_exception(datetime(year=2018, month=11, day=14), trip, service_id)
            wrap_add_trip_if_no_exception(datetime(year=2018, month=11, day=22), trip, service_id)

        self.assertEqual(tuple(expected_date_trip_dict.keys()), tuple(valid_trips_dict.keys()))

        for key in expected_date_trip_dict:
            self.assertTrue(expected_date_trip_dict[key].issubset(valid_trips_dict[key]))
            self.assertTrue(valid_trips_dict[key].issubset(expected_date_trip_dict[key]))

    def test_add_trip_if_valid_day_of_week(self):
        valid_trips_dict = {
            datetime(year=2018, month=11, day=13): set()
        }

        expected_date_trip_dict = {
            datetime(year=2018, month=11, day=13): {'t3'}
        }

        for trip in self.TEST_TRIP_DICT:
            add_trip_if_valid_day_of_week(
                self.TEST_SERVICE_DATES_DICT[self.TEST_TRIP_DICT[trip].serviceId].serviceDays,
                date_helpers.to_day_of_week(datetime(year=2018, month=11, day=13).weekday()),
                valid_trips_dict,
                datetime(year=2018, month=11, day=13),
                trip
            )

        self.assertEqual(tuple(expected_date_trip_dict.keys()), tuple(valid_trips_dict.keys()))

        for key in expected_date_trip_dict:
            self.assertTrue(expected_date_trip_dict[key].issubset(valid_trips_dict[key]))
            self.assertTrue(valid_trips_dict[key].issubset(expected_date_trip_dict[key]))
