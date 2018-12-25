import os

import csv
from datetime import datetime

from gtfs_parsing.read_data.csv_reading_helper_functions import separate_columns_from_data
from gtfs_parsing.data_structures.data_structures import serviceDates


def read_dates(agency, date):
    return read_calendar(agency, date), read_calendar_dates(agency, date)


def read_calendar(agency, date):
    with open(os.path.join('./agencies', agency, 'data', date, 'calendar.txt')) as f:
        unformatted_calendar = csv.reader(f, delimiter=',')
        calendar_namedtuple = separate_columns_from_data(unformatted_calendar)
        return create_service_start_end_date_dict(calendar_namedtuple.data, calendar_namedtuple.columns)


def read_calendar_dates(agency, date):
    with open(os.path.join('./agencies', agency, 'data', date, 'calendar_dates.txt')) as f:
        unformatted_calendar_dates = csv.reader(f, delimiter=',')
        calendar_dates_namedtuple = separate_columns_from_data(unformatted_calendar_dates)
        return create_calendar_exceptions_dict(calendar_dates_namedtuple.data, calendar_dates_namedtuple.columns)


def create_service_start_end_date_dict(date_ranges, date_columns):
    start_end_date_dict = dict()

    for date_range in date_ranges:
        start_end_date_dict[date_range[date_columns['service_id']]] = serviceDates(
            start_date=datetime.strptime(date_range[date_columns['start_date']], '%Y%m%d'),
            end_date=datetime.strptime(date_range[date_columns['end_date']], '%Y%m%d'),
            serviceDays=parse_service_days(date_range, date_columns)
        )

    return start_end_date_dict


def parse_service_days(date_range, date_columns):
    return {
        'm': parse_service_day(date_range[date_columns['monday']]),
        't': parse_service_day(date_range[date_columns['tuesday']]),
        'w': parse_service_day(date_range[date_columns['wednesday']]),
        'r': parse_service_day(date_range[date_columns['thursday']]),
        'f': parse_service_day(date_range[date_columns['friday']]),
        's': parse_service_day(date_range[date_columns['saturday']]),
        'u': parse_service_day(date_range[date_columns['sunday']])
    }


def create_calendar_exceptions_dict(exceptions, exceptions_columns):
    exceptions_dict = dict()

    for exception in exceptions:
        if exception[exceptions_columns['service_id']] not in exceptions_dict:
            exceptions_dict[exception[exceptions_columns['service_id']]] = dict()

        exceptions_dict[exception[exceptions_columns['service_id']]][
            datetime.strptime(exception[exceptions_columns['date']], '%Y%m%d')] = \
            parse_exception_type(exception[exceptions_columns['exception_type']])

    return exceptions_dict


def parse_service_day(service_day):
    if service_day == '1':
        return True
    if service_day == '0':
        return False
    raise ValueError("Presence of service must be indicated using 0 or 1")


def parse_exception_type(exception_type):
    if exception_type == '1':
        return True
    if exception_type == '2':
        return False
    raise ValueError("Exception type must be either 1 or 2.")
