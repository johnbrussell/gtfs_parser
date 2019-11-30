This is a GTFS parser tailored to be used with [gtfs-traversal](https://github.com/johnbrussell/gtfs-traversal).

# Usage

Typically, something like this: 
```python
from gtfs_parser.gtfs_parsing.analyses import determine_analysis_parameters, get_unique_route_trip_dict

configurations = determine_analysis_parameters(config)
configuration_to_analyze = configurations[0]  # choose appropriate index

data = get_unique_route_trip_dict(configuration_to_analyze, data_location)
```
where `config` is a dictionary that stores information about what you need parsed (more on that below) and `data_location` is the file path to the folder containing the folder for the GTFS data for the agency whose data is in the `configuration_to_analyze`. 

# Config

The `config` variable in the example above typically looks something like this: 
```python
{
  "agencies": {
    "mbta": {
      "data_sets": {
        "2018-10-13": {
          "start_date": "2018-10-13",
          "end_date": "2018-10-19",
          "route_types_to_solve": [0, 1]
        }
      }
    }
  }
}
```
In the example: 
 - `mbta` is an example of the names of agencies you'd like to parse.
 - `2018-10-13` is the date associated with the suite of GTFS data. 
 - `start_date` and `end_date` define the range of days whose data will be parsed.  These dates' data are included in the parsing. 
 - `route_types_to_solve` is a list of the [types](https://developers.google.com/transit/gtfs/reference#routestxt) of route to parse. Currently, as long as the list is not empty, the parser will parse all routes.
 
 # Data storage
 
 This parser requires you to store your GTFS data in a very particular way that, if honored, can allow for parsing of multiple GTFS time periods for multiple agencies in one call to `determine_analysis_parameters`.  The format is this: if you're storing data for the MBTA for 1/1/2018 and 2/1/2018, as well as the Pittsburgh Port Authority for 4/1/2018, you'd store it like this: 
 ```python
folder_containing_data
 |_ mbta
 |   |_ data
 |       |_ 2018-01-01
 |       |   |_ [all the .txt files]
 |       |_ 2018-02-01
 |           |_ [all the .txt files]
 |_ pittsburgh_port_authority
     |_ data
         |_ 2018-04-01
             |_ [all the .txt files]
```
You get to define the names of the transit agencies and the dates of the data, but the folder name `data` must appear exactly as in the example and the .txt files must have the standard names and should not be formatted differently than the GTFS standard. 
