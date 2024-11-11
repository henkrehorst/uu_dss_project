import pandas as pd
import os
from sqlalchemy import create_engine
from data.ns.ns_rail_route_geo_json import rail_stops, get_geo_json, getStationName
import json


def import_frequent_rail_routes():
    engine = create_engine(os.getenv('DATABASE_URL'))
    table_name = 'ns_frequent_rail_routes'

    # read frequent rail routes json_data file
    frequent_rail_routes = pd.read_json('./data/ns/json_data/frequent_ns_routes.json')

    # iterate through the frequent rail routes and add the geojson data
    for index, row in frequent_rail_routes.iterrows():
        # Get a list of intermediate stops between the from and to station
        station_data = rail_stops(row['fromStation'], row['toStation'])
        # Convert the list of intermediate stations to a string so that it fits the getGeo API
        station_data_formatted = ",".join(station_data)
        # Get the GeoJSon for the given route
        geo_json_route = get_geo_json(station_data_formatted)
        geo_json_route[0]['styles'] = {'color': row['color']}
        geo_json_route[0]['stations'] = [getStationName(row['fromStation']), getStationName(row['toStation'])]

        frequent_rail_routes.at[index, 'geojson'] = json.dumps(geo_json_route)

    # save frequent rail routes to database
    frequent_rail_routes.to_sql(table_name, engine, if_exists='replace', index=False)

    print(f"NS Frequent rail routes imported successfully")
