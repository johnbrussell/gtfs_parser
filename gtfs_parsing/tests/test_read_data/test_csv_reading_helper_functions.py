import csv
import os
import unittest

import numpy as np

from gtfs_parsing.read_data.csv_reading_helper_functions import coerce_integer_to_string, create_csv_column_dict


class TestDataMunging(unittest.TestCase):
    def test_csv_column_dict(self):
        with(open(os.path.join('./gtfs_parsing', 'tests', 'test_csv_files', 'test_routes.txt'))) as f:
            reader = csv.reader(f, delimiter=',')
            column = next(reader)
        expected_output = {
            'route_id': 0,
            'agency_id': 1,
            'route_short_name': 2,
            'route_long_name': 3,
            'route_desc': 4,
            'route_type': 5,
            'route_url': 6,
            'route_color': 7,
            'route_text_color': 8,
            'route_sort_order': 9,
        }
        actual_output = create_csv_column_dict(column)

        for key in actual_output:
            self.assertIn(key, expected_output)
            self.assertTrue(actual_output[key] == expected_output[key])
        for key in expected_output:
            self.assertIn(key, actual_output)

    def test_coerce_integer_to_string(self):
        self.assertEqual(coerce_integer_to_string("1.0"), "1")
        self.assertEqual(coerce_integer_to_string("1.1"), "1.1")
        self.assertEqual(coerce_integer_to_string(np.nan), "nan")
        self.assertEqual(coerce_integer_to_string(""), "UNKNOWN")
        self.assertEqual(coerce_integer_to_string("1"), "1")
