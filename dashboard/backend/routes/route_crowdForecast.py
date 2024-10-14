import os

from flask import Blueprint, abort
import requests
import json
import numpy as np

crowd_forecast_blueprint = Blueprint('crowd_forecast', __name__)


@crowd_forecast_blueprint.route('/crowd_forecast')
def getCrowdForecast(from_station, to_station):

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
    }

    # Send GET request
    try:
        # Returns JSON file with nearest train station(s) of the put in lat/long
        response = requests.get(url, headers=headers, params=params)
        # Parse JSON content
        crowd_data = response.json()

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # e.g., 404 Not Found


    converted_crowd_data = crowd_data['trips'][0]['crowdForecast']

    if converted_crowd_data == "LOW":
        return "#44984c" # Green
    elif converted_crowd_data == "MEDIUM":
        return "#ee8031" # Orange
    elif converted_crowd_data == "HIGH":
        return "#c92a32" # Red
    else:
        return "#000000"