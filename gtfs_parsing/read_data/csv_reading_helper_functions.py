import re

from gtfs_parsing.data_structures.data_structures import dataWithColumns


# Feels like I'm reinventing the wheel with this file.  In a more formal setting, I'd try to find a
#  library that performs this functionality.


def separate_columns_from_data(data_gen):
    # data_gen is a generator of the data from the CSV file that is the input.  This function separates that
    #  generator into its first element (ie., the columns of the data) and the rest of the data.
    columns = next(data_gen)
    data = dataWithColumns(data=data_gen, columns=create_csv_column_dict(columns))
    return data


def create_csv_column_dict(columns):
    # Takes the first row of a CSV file (ie., the columns).  Returns dict(column_name: index_in_row).
    column_index = 0
    column_indices = dict()
    for name in columns:
        column_indices[name] = column_index
        column_index += 1
    return column_indices


def coerce_integer_to_string(seq):
    # The goal here is to coerce values from the 'stop_sequence' column of `stop_times.txt` to string.
    #  These values should be integers in the raw data.  Since python likes to add trailing ".0"s to the end of
    #  numeric values when converting from unspecified numeric value to string, I must replace those, while
    #  accommodating the case where the column contains an empty value
    return re.sub("\.0", "", str(seq)) if seq else "UNKNOWN"
