import os

import googlemaps
from datetime import datetime
import requests
import geojson
import pandas as pd
from googlemaps.convert import decode_polyline
import json
from sqlalchemy import create_engine


def import_rail_routes_car_times_by_google_maps():
    # get all rail routes from database
    engine = create_engine(os.getenv('DATABASE_URL'))

    frequent_rail_routes = pd.read_sql_query(
        f"select id, name, from_station, to_station, from_coordinates, to_coordinates,  color from ns_frequent_rail_routes",
        engine)

    rail_route_car_times = list()

    # iterate over all rail routes
    for index, row in frequent_rail_routes.iterrows():
        # get travel time by car
        travel_time = get_car_travel_time(row['from_coordinates'], row['to_coordinates'])

        # append to list
        rail_route_car_times.append({
            'rail_route_name': row['name'],
            'from_station': row['from_station'],
            'to_station': row['to_station'],
            'duration_in_minutes': travel_time,
            'car_geo_json': get_route_geojson(row['from_coordinates'], row['to_coordinates']),
            'road_distance': get_road_distance(row['from_coordinates'], row['to_coordinates'])
        })

    # save rail route car times to database
    pd.DataFrame(rail_route_car_times) \
        .to_sql('rail_route_car_comparison', engine, if_exists='replace', index=False)


def get_car_travel_time(origin, destination):
    gmaps = googlemaps.Client(key="AIzaSyB-VAWpVIXpKZqjJW1wDf_gZwJZ00P9RPY")

    # here the request for to the google maps api is made for driving directions
    directions = gmaps.directions(origin, destination, mode="driving", departure_time=datetime.now())
    travel_time = directions[0]['legs'][0]['duration'][
                      'value'] / 60  # This Converts every time given from seconds to minutes
    return travel_time


def get_road_distance(fromCoordinates, toCoordinates):
    gmaps = googlemaps.Client(key="AIzaSyB-VAWpVIXpKZqjJW1wDf_gZwJZ00P9RPY")

    result = gmaps.distance_matrix(origins=(fromCoordinates), destinations=(toCoordinates), mode='driving')

    distresult = result["rows"][0]["elements"][0]["distance"]["value"] / 1000  # Convert to KM by /1000

    return round(distresult, 1)


def get_route_geojson(start, end):
    start = tuple(start.split(","))
    end = tuple(end.split(","))
    # Construct the request URL
    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={start[0]},{start[1]}&destination={end[0]},{end[1]}&key=AIzaSyB-VAWpVIXpKZqjJW1wDf_gZwJZ00P9RPY"

    # Make the request to the Directions API
    response = requests.get(url)
    directions = response.json()

    # Check if the request was successful
    if directions['status'] != 'OK':
        raise Exception(f"Error in Directions API request: {directions['status']}")

    # Extract polyline and decode it
    route_polyline = directions['routes'][0]['overview_polyline']['points']
    decoded_points = decode_polyline(route_polyline)

    # Create GeoJSON Feature
    route_line = geojson.LineString([(point['lng'], point['lat']) for point in decoded_points])
    route_feature = geojson.Feature(geometry=route_line, properties={"name": "Route"})

    # Return as GeoJSON FeatureCollection
    return json.dumps(geojson.FeatureCollection([route_feature]))
