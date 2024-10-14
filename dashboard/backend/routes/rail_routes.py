import os

from flask import Blueprint, abort
import requests
import json
import numpy as np

rail_routes_blueprint = Blueprint('rail_routes', __name__)


@rail_routes_blueprint.route("/rail_routes/lines")
def get_rail_routes_lines():
    return [
        {
            "id": "1",
            "name": "Zaandam – Schiphol ",
            "fromStation": "zd",
            "toStation": "shl"
        },
        {
            "id": "2",
            "name": "Hoorn – Zaandam ",
            "fromStation": "hn",
            "toStation": "zd"
        },
        {
            "id": "3",
            "name": "Amsterdam Centraal – Hilversum ",
            "fromStation": "asd",
            "toStation": "hvs"
        },
        {
            "id": "4",
            "name": "Tilburg – ’s Hertogenbosch ",
            "fromStation": "tb",
            "toStation": "ht"
        },
        {
            "id": "5",
            "name": "Hilversum – Schiphol ",
            "fromStation": "hvs",
            "toStation": "shl"
        },
        {
            "id": "6",
            "name": "Schiphol – Almere Centrum ",
            "fromStation": "shl",
            "toStation": "alm"
        },
        {
            "id": "7",
            "name": "Amsterdam Centraal – Hoorn ",
            "fromStation": "asd",
            "toStation": "hn"
        },
        {
            "id": "8",
            "name": "Utrecht – ’s Hertogenbosch ",
            "fromStation": "ut",
            "toStation": "ht"
        }
    ]

@rail_routes_blueprint.route('/rail_routes')
def rail_routes():
    print(get_rail_routes_lines())
    stations = get_rail_routes_lines()

    def getGeo(StationList):
        # This function fetches geodata based on a list of interlinked stations

        # Primary Key from NS API
        primary_key = "0c97e49d1a0e4a10bb2313d4bb697472"

        # Placeholder for the URL
        url = "https://gateway.apiportal.ns.nl/Spoorkaart-API/api/v1/traject"

        # Headers as defined in NS API documentation
        headers = {
            "Cache-Control": "no-cache",
            "Ocp-Apim-Subscription-Key": primary_key
        }

        # Parameters as defined in NS API documentation
        params = {
            "stations": StationList #List of all intermediate stations on the railroute
        }

        # Send GET request
        try:
            # Returns JSON file with nearest train station(s) of the put in lat/long
            response = requests.get(url, headers=headers, params=params)
            # Parse JSON content
            stations_data = response.json()

        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")  # e.g., 404 Not Found

        return stations_data['payload']['features']

    def random_color_generator():
        color = (np.random.randint(0, 256),np.random.randint(0, 256),np.random.randint(0, 256))
        return tuple(color)

    TotalJson = []
    for station in stations: # Loop through all rows in the list of stations to plot named "Stations"
        stationData= rail_stops(station['fromStation'], station['toStation']) # Get a list of intermediate stops between the from and to station
        stationDataFormatted = ",".join(stationData) # Convert the list of intermediate stations to a string so that it fits the getGeo API
        GeoJsonRoute = getGeo(stationDataFormatted) # Get the GeoJSon for the given route
        TotalJson.append(GeoJsonRoute)  # Add the GeoJson to a combined list

    return json.dumps(TotalJson)


@rail_routes_blueprint.route('/rail_stops')
def rail_stops(from_station, to_station):
    # This function fetches a list of intermediate stops between the from and to station

    # Primary Key from NS API
    primary_key = "0c97e49d1a0e4a10bb2313d4bb697472"

    # Placeholder for the URL
    url = "https://gateway.apiportal.ns.nl/reisinformatie-api/api/v3/trips"

    # Headers as defined in NS API documentation
    headers = {
        "Cache-Control": "no-cache",
        "Ocp-Apim-Subscription-Key": primary_key
    }

    # Parameters as defined in NS API documentation
    params = {
        "fromStation": from_station,
        "toStation": to_station,
        "passing": True #Shows intermediate stations
    }

    # Send GET request
    try:
        # Returns JSON file with nearest train station(s) of the put in lat/long
        response = requests.get(url, headers=headers, params=params)
        # Parse JSON content
        stops_data = response.json()

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # e.g., 404 Not Found

    # The rail_stops() function originally returns a list of station names, subsequent API's use list of Stationcodes, so called FE_codes
    def convert_stop_data(data):
        converted_data = []
        for stop in data['trips'][0]['legs'][0]['stops']:
            converted_data.append(FE_Codes(stop['name']))

        return converted_data

    converted_stop_data = convert_stop_data(stops_data) #uses the convert_stop_data to loop through every stationname and convert it to FE_codes

    return converted_stop_data

# Converts the station name to the station code or FE_code captured by the NS api
def FE_Codes(StationName):

    # Primary Key from NS API
    primary_key = "0c97e49d1a0e4a10bb2313d4bb697472"

    # Placeholder for the URL
    url = "https://gateway.apiportal.ns.nl/reisinformatie-api/api/v2/stations"

    # Headers as defined in NS API documentation
    headers = {
        "Cache-Control": "no-cache",
        "Ocp-Apim-Subscription-Key": primary_key
    }

    # Parameters as defined in NS API documentation
    params = {
        "q": StationName
    }

    # Send GET request
    try:
        # Returns JSON file with nearest train station(s) of the put in lat/long
        response = requests.get(url, headers=headers, params=params)
        # Parse JSON content
        FE_data = response.json()

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # e.g., 404 Not Found

    StationCode = str(FE_data['payload'][0]['code']) # Returns the FE_code as a string

    return StationCode
