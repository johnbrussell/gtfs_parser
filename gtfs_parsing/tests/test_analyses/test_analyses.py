import unittest

from gtfs_parsing.analyses.analyses import determine_analysis_parameters
from gtfs_parsing.data_structures.data_structures import runConfiguration


class TestDataMunging(unittest.TestCase):
    def testExtractAllRunParametersFromConfig(self):
        fake_config = {
          "agencies": {
            "mbta": {
              "data_sets": {
                "2018-10-13": {
                  "start_date": "2018-10-13",
                  "end_date": "2018-10-19",
                  "route_types_to_solve": [0, 1]
                }
              }
            },
            "pittsburgh_port_authority": {
              "data_sets": {
                "2018-08-08": {
                  "start_date": "2018-09-04",
                  "end_date": "2018-09-10",
                  "route_types_to_solve": [1, 7]
                }
              }
            }
          }
        }
        expected_run_parameter_list = [runConfiguration(agency='mbta', date='2018-10-13', start_date="2018-10-13",
                                                        end_date="2018-10-19", route_types=[0, 1]),
                                       runConfiguration(agency='pittsburgh_port_authority', date='2018-08-08',
                                                        start_date="2018-09-04", end_date="2018-09-10",
                                                        route_types=[1, 7])]
        actual_run_parameter_list = determine_analysis_parameters(fake_config)

        for expected_config, actual_config in zip(expected_run_parameter_list, actual_run_parameter_list):
            self.assertEqual(expected_config, actual_config)
