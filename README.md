# gtfs_parser
  
This is a GTFS parser.  I built it to be used with [gtfs-traversal](https://github.com/johnbrussell/gtfs-traversal), but it can be used for more general purposes.  Its main feature is that it amalgamates the data in ways that: 
 - allow for easy access to information about a particular trip, without having to reference multiple GTFS files to do so. 
 - allow for easy iteration across many trips.
 - remove the need to rely on pandas, whose `DataFrame`s are slow over multiple successive queries for information about a particular resource.

# Usage

Typically, something like this: 
```python
from gtfs_parser.gtfs_parsing.analyses import determine_analysis_parameters, parse

configurations = determine_analysis_parameters(config)
configuration_to_analyze = configurations[0]  # choose appropriate index

data = parse(configuration_to_analyze, data_location)
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
 
 # Output
 
 In the usage example, the return value is assigned to a variable called `data` is returned.  This return value is a namedtuple of type `gtfsSchedules`.  Each `gtfsSchedules` has three parts: `tripSchedules`, `dateTrips`, and `uniqueRouteTrips`. 
 
 ## tripSchedules
 
 `tripSchedules` holds a dictionary.  The keys are the `trip_id`s of each individual trip in the stop_times.txt dataset.  The values are namedtuples of type `tripInfo`.  A `tripInfo` namedtuple has three parts, `tripStops`, `tripRouteInfo`, and `serviceId`.  
 
 `tripStops` is a dictionary where the keys are the values from the stop_times.txt file's `stop_sequence` column and the values are namedtuples of type `stopDeparture`.  A `stopDeparture` has two fields, `stopId`, which is the stop's `stop_id` in the dataset, and `departure_time`, which is the stop's `departure_time` in the dataset. 
 
 `tripRouteInfo`, the field in the `tripInfo` namedtuple, is a namedtuple of type `routeInfo`.  A `routeInfo` namedtuple has two fields, `routeId` and `routeType`, which correspond to the `route_id` and `route_type` fields for the corresponding route in the routes.txt file.
 
 The `serviceId` field in the `tripInfo` is the value of `service_id` for the trip in the trips.txt file. 
 
 ## dateTrips
 
 `dateTrips` is a dictionary where the keys are `datetime` objects representing unique days (ie., the `year`, `month`, and `day` attributes are filled out but everything is is zero); the values are `set`s of `trip_id`s operating on that service day. 
 
 ## uniqueRouteTrips
 
 `uniqueRouteTrips` is a dictionary.  The keys are unique integers.  The values are namedtuples of type `uniqueRouteInfo`.  
 
 The `uniqueRouteInfo` namedtuple has `tripIds` and `routeInfo`.  `tripIds` is a `list` of `trip_id`s from trips.txt.  `routeInfo` is a namedtuple of type `routeInfo`. 
 
 The `routeInfo` namedtuple has `routeId`, which is a `route_id` in the routes.txt file, and `routeType` is that route's `route_type` from the routes.txt file.  All trips in the `tripIds` list will correspond with the route of this `route_id`. 
 
 The purpose of this dictionary is to differentiate between the various variations of each route.  So, for each key in the `uniqueRouteTrips` dictionary, all `trips` in the value's `tripIds` field will have exactly the same set of stops in exactly the same order.
 
 ## stopLocations
 
 `stopLocations` is a dictionary.  The keys are stop IDs.  The values are `stopLocation` namedtuples where the `lat` attributes are the latitudes of the stops and the `long` attributes are the longitudes of the stops.
 
 ## Visualization
 
 Collectively these outputs allow for easy access to information about a particular trip, or iteration over many trips, in a way that does the work of combining useful information from the various input tables into one place and returns a data structure that is easier and faster to work with than a pandas data frame. The output looks something like this: 
```python
data = gtfsSchedules(
    tripSchedules={
        'CR-Saturday-Fall-17-1752': tripInfo(
            tripStops={
                '1': stopDeparture(stopId='Readville', departureTime='7:30:00'),
                '2': stopDeparture(stopId='Fairmount', departureTime='7:33:00'),
                # more stops
            },
            tripRouteInfo=routeInfo(routeId='CR-Fairmount', routeType='2'),
            serviceId='CR-Saturday-SouthSide-Fall-17-FMT'
        ),
        # more trips
    },
    dateTrips={
        datetime(year=2018, month=11, day=20): {'CR-Saturday-Fall-17-1752', ... },
        # more dates
    },
    uniqueRouteTrips={
        1: uniqueRouteInfo(tripIds=['CR-Saturday-Fall-17-1752', ... ], routeInfo=routeInfo(routeId="CR-Fairmount", routeType="2")),
        # more unique routes
    },
    stopLocations={
        'stop-1': stopLocation(lat=0.0, long=0.0),
        # more stops
    }
)
```
  
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
