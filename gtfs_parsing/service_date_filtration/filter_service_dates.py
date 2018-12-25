from datetime import datetime, timedelta

from gtfs_parsing.read_data import read_date_information
from gtfs_parsing.service_date_filtration import date_helpers


def filter_for_service_dates(agency, date, trips_dict, start_date, end_date):
    normal_service_dates, service_exceptions = read_date_information.read_dates(agency, date)
    return to_date_trip_dict(trips_dict, start_date, end_date, normal_service_dates,
                             service_exceptions)


def to_date_trip_dict(trips_dict, start_date, end_date, normal_service_dates, service_exceptions):
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')

    current_date = start_date
    valid_trips_dict = dict()

    while current_date <= end_date:
        valid_trips_dict[current_date] = set()

        find_valid_trips(trips_dict, normal_service_dates, start_date, end_date, current_date, service_exceptions,
                         valid_trips_dict)

        current_date += timedelta(days=1)

    return valid_trips_dict


def find_valid_trips(trips_dict, normal_service_dates, start_date, end_date, current_date, service_exceptions,
                     valid_trips_dict):
    current_day_of_week = date_helpers.to_day_of_week(current_date.weekday())

    for trip in trips_dict:
        service_id = trips_dict[trip].serviceId
        service_start_date = normal_service_dates[service_id].start_date
        service_end_date = normal_service_dates[service_id].end_date

        if date_outside_of_service_range(current_date, start_date, service_end_date, service_start_date, end_date):
            continue

        add_trip_if_valid(normal_service_dates, service_id, service_exceptions, current_day_of_week,
                          valid_trips_dict, current_date, trip)


def date_outside_of_service_range(current_date, start_date, service_end_date, service_start_date, end_date):
    return start_date > service_end_date or end_date < service_start_date or \
        current_date < service_start_date or current_date > service_end_date


def add_trip_if_valid_day_of_week(service_days_of_week, current_day_of_week, valid_dict, current_date, trip):
    if service_days_of_week[current_day_of_week]:
        valid_dict[current_date].add(trip)


def add_trip_if_no_exception(service_exceptions, service_id, current_date, service_days_of_week, current_day_of_week,
                             valid_trips, trip):
    if current_date not in service_exceptions[service_id]:
        add_trip_if_valid_day_of_week(service_days_of_week, current_day_of_week, valid_trips, current_date,
                                      trip)
    if current_date in service_exceptions[service_id]:
        if service_exceptions[service_id][current_date]:
            valid_trips[current_date].add(trip)


def add_trip_if_valid(service_dates, service_id, service_exceptions, current_day_of_week, valid_trips, current_date,
                      trip):
    service_days_of_week = service_dates[service_id].serviceDays

    if service_id in service_exceptions:
        add_trip_if_no_exception(service_exceptions, service_id, current_date, service_days_of_week,
                                 current_day_of_week, valid_trips, trip)
    else:
        add_trip_if_valid_day_of_week(service_days_of_week, current_day_of_week, valid_trips, current_date,
                                      trip)
