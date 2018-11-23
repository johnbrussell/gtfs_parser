from gtfs_parsing.read_data import read_routes, read_stop_times, read_trips
from gtfs_parsing.data_structures.data_structures import runConfiguration
from gtfs_parsing.unique_route_determination import determine_unique_routes


def run_analyses(config):
    for configuration in determine_analysis_parameters(config):
        run_analysis(configuration)


def run_analysis(configuration):
    print("Running {agency} data from {date}".format(agency=configuration.agency, date=configuration.date))
    trip_type_stop_time_dict = read_stop_times.read_stop_times(configuration.agency, configuration.date,
                                                               get_trip_type_dict(configuration.agency,
                                                                                  configuration.date))
    unique_route_trip_dict = determine_unique_routes.to_unique_route_trip_dict(trip_type_stop_time_dict)
    print(len(unique_route_trip_dict))


def determine_analysis_parameters(config):
    configurations = list()
    for agency in config['agencies']:
        for date in config['agencies'][agency]['data_sets']:
            route_types_to_solve = (config['agencies'][agency]['data_sets'][date]).get('route_types_to_solve', list())
            if len(route_types_to_solve) > 0:
                print("Running {agency} data from {date}".format(agency=agency, date=date))
                start_date = (config['agencies'][agency]['data_sets'][date]).get('start_date', None)
                end_date = (config['agencies'][agency]['data_sets'][date]).get('end_date', None)
                configurations.append(runConfiguration(agency=agency, date=date, start_date=start_date,
                                                       end_date=end_date, route_types=route_types_to_solve))
    return configurations


def get_trip_type_dict(agency, date):
    route_type_dict = read_routes.read_routes(agency, date)
    return read_trips.read_trip_types(agency, date, route_type_dict)
