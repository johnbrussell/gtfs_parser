def get_trip_type_dict():
    route_type_dict = read_routes.read_routes()
    return read_trips.read_trip_types(route_type_dict)


if __name__ == "__main__":
    from gtfs_parsing import read_stop_times, read_routes, read_trips

    trip_stop_dict = read_stop_times.read_stop_times(get_trip_type_dict())
