import requests


def rail_stops_and_trip_duration(from_station, to_station):
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
        "passing": True  # Shows intermediate stations
    }

    # Send GET request
    try:
        # Returns JSON file with nearest train station(s) of the put in lat/long
        response = requests.get(url, headers=headers, params=params)
        # Parse JSON content
        stops_data = response.json()

        # This part retrieves all the possible routes from the trips api and searches for the 'plannedDurationInMinutes' in the api
        trips = stops_data.get('trips', [])
        travel_times = [trip['plannedDurationInMinutes'] for trip in trips]
        # Here the avarage train times are calculated
        avg_train_time = sum(travel_times) / len(travel_times) if travel_times else None

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # e.g., 404 Not Found

    # The rail_stops() function originally returns a list of station names, subsequent API's use list of Stationcodes, so called FE_codes
    def convert_stop_data(data):
        converted_data = []
        for stop in data['trips'][0]['legs'][0]['stops']:
            converted_data.append(FE_Codes(stop['name']))

        return converted_data

    converted_stop_data = convert_stop_data(
        stops_data)  # uses the convert_stop_data to loop through every stationname and convert it to FE_codes

    return converted_stop_data, avg_train_time


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

    StationCode = str(FE_data['payload'][0]['code'])  # Returns the FE_code as a string

    return StationCode


# This function fetches geodata based on a list of interlinked stations
def get_geo_json(StationList):
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
        "stations": StationList  # List of all intermediate stations on the railroute
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


def get_station_information(UcCode):
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
        "q": UcCode
    }

    # Send GET request
    try:
        response = requests.get(url, headers=headers, params=params)
        # Parse JSON content
        Station_data = response.json()

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # e.g., 404 Not Found

    StationName = str(Station_data['payload'][0]['namen']['middel'])  # Returns the StationName as a string
    latitude = str(Station_data['payload'][0]['lat'])
    longitude = str(Station_data['payload'][0]['lng'])
    coordinates = (latitude + "," + longitude)

    return StationName, coordinates


def get_tariff_units(fromStation, toStation):
    # Primary Key from NS API
    primary_key = "506c530bc78e42238652c7ffba855a3c"

    # Placeholder for the URL
    url = "https://gateway.apiportal.ns.nl/public-prijsinformatie/prices"

    # Headers as defined in NS API documentation
    headers = {
        "Cache-Control": "no-cache",
        "Ocp-Apim-Subscription-Key": primary_key
    }

    # Specifying the from and to stations for a route
    params = {
        "fromStation": fromStation,
        "toStation": toStation
    }

    # Send GET request
    try:
        # Returns JSON file with nearest train station(s) of the put in lat/long
        response = requests.get(url, headers=headers, params=params)
        # Parse JSON content
        stations_data = response.json()

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # e.g., 404 Not Found

    return stations_data['priceOptions'][1]['tariefEenheden']
