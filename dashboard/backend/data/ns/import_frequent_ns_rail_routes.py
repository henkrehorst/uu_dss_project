import pandas as pd
import os
from sqlalchemy import create_engine
from data.ns.ns_api import rail_stops_and_trip_duration, get_geo_json, get_station_information
import json


def import_frequent_rail_routes():
    engine = create_engine(os.getenv('DATABASE_URL'))
    table_name = 'ns_frequent_rail_routes'

    # read frequent rail routes json_data file
    frequent_rail_routes = pd.read_json('./data/ns/json_data/frequent_ns_routes.json')

    # iterate through the frequent rail routes and add the geojson data and travel duration
    for index, row in frequent_rail_routes.iterrows():
        # Get a list of intermediate stops between the from and to station
        station_data, duration = rail_stops_and_trip_duration(row['from_station'], row['to_station'])
        # Convert the list of intermediate stations to a string so that it fits the getGeo API
        station_data_formatted = ",".join(station_data)

        from_station_name, from_coordinates = get_station_information(row['from_station'])
        to_station_name, to_coordinates = get_station_information(row['to_station'])
        # Get the GeoJSon for the given route
        geo_json_route = get_geo_json(station_data_formatted)
        geo_json_route[0]['styles'] = {'color': row['color']}
        geo_json_route[0]['stations'] = [from_station_name, to_station_name]

        frequent_rail_routes.at[index, 'geojson'] = json.dumps(geo_json_route)
        frequent_rail_routes.at[index, 'trip_duration'] = duration
        frequent_rail_routes.at[index, 'from_coordinates'] = from_coordinates
        frequent_rail_routes.at[index, 'to_coordinates'] = to_coordinates

    # save frequent rail routes to database
    frequent_rail_routes.to_sql(table_name, engine, if_exists='replace', index=False)

    print(f"NS Frequent rail routes imported successfully")
