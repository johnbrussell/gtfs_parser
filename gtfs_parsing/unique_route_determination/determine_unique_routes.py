from gtfs_parsing.data_structures.data_structures import uniqueRouteInfo


def to_unique_route_trip_dict(trip_type_stop_time_dict):
    unique_route_trip_dict = dict()

    for trip_id in trip_type_stop_time_dict:
        trip_route_info = get_trip_route_info(trip_id, trip_type_stop_time_dict)

        known_route, route_id = identify_known_route(unique_route_trip_dict, trip_route_info, trip_id,
                                                           trip_type_stop_time_dict)

        if not known_route:
            add_unique_route(unique_route_trip_dict, route_id, trip_route_info)

        place_trip_into_unique_routes_dict(unique_route_trip_dict, route_id, trip_id)

    return unique_route_trip_dict


def identify_known_route(unique_route_trip_dict, trip_route_info, trip_id, trip_type_stop_time_dict):
    for route_id in unique_route_trip_dict:
        route_route_info = get_route_route_info(route_id, unique_route_trip_dict)

        if not route_types_match(trip_route_info, route_route_info):
            continue

        if not all_stops_match(trip_id, route_id, trip_type_stop_time_dict, unique_route_trip_dict):
            continue

        return True, route_id
    return False, len(unique_route_trip_dict) + 1


def add_unique_route(unique_route_trip_dict, new_route_id, trip_route_info):
    unique_route_trip_dict[new_route_id] = uniqueRouteInfo(tripIds=list(), routeInfo=trip_route_info)


def place_trip_into_unique_routes_dict(unique_route_trip_dict, new_route_id, new_trip_id):
    unique_route_trip_dict[new_route_id].tripIds.append(new_trip_id)


def get_trip_route_info(trip, trip_dict):
    return trip_dict[trip].tripRouteInfo


def get_route_route_info(route, route_dict):
    return route_dict[route].routeInfo


def route_types_match(trip_route_type, route_route_type):
    return trip_route_type == route_route_type


def all_stops_match(trip_id, route_id, trip_dict, route_dict):
    trip_stops = get_trip_stops(trip_dict, trip_id)

    route_first_trip_id = route_dict[route_id].tripIds[0]
    known_trip_stops = get_trip_stops(trip_dict, route_first_trip_id)

    if len(trip_stops) != len(known_trip_stops):
        return False
    return is_list_of_identical_tuples(zip(trip_stops, known_trip_stops))


def is_list_of_identical_tuples(list_of_two_tuples):
    for tup in list_of_two_tuples:
        if tup[0] != tup[1]:
            return False
    return True


def get_trip_stops(trip_dict, trip_id):
    trip_stops = trip_dict[trip_id].tripStops.values()
    return [stop.stopId for stop in trip_stops]
