import os

from flask import Blueprint, abort
import requests
import json
import numpy as np

station_name_blueprint = Blueprint('station_name', __name__)


@station_name_blueprint.route('/station_name')
def getStationName(UcCode):
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

    return StationName 