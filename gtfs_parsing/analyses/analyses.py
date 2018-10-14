from gtfs_parsing.read_data import read_routes, read_stop_times, read_trips
from gtfs_parsing.data_structures.data_structures import runConfiguration


def run_analyses(config):
    for configuration in determine_analysis_parameters(config):
        run_analysis(configuration.agency, configuration.date, config)


def run_analysis(agency, date, config):
    print("Running {agency} data from {date}".format(agency=agency, date=date))
    trip_stop_dict = read_stop_times.read_stop_times(agency, date, get_trip_type_dict(agency, date))


def determine_analysis_parameters(config):
    configurations = list()
    for agency in config['agencies']:
        for date in config['agencies'][agency]['data_sets']:
            if len((config['agencies'][agency]['data_sets'][date]).get('route_types_to_solve', list())) > 0:
                print("Running {agency} data from {date}".format(agency=agency, date=date))
                configurations.append(runConfiguration(agency=agency, date=date))
    return configurations


def get_trip_type_dict(agency, date):
    route_type_dict = read_routes.read_routes(agency, date)
    return read_trips.read_trip_types(agency, date, route_type_dict)
