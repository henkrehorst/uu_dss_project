import os

from flask import Blueprint, abort
import requests
import json
import numpy as np

rail_routes_blueprint = Blueprint('rail_routes', __name__)


@rail_routes_blueprint.route("/rail_routes")
def get_rail_routes():
    # Send GET request
    try:
        # Returns JSON file with nearest train station(s) of the put in lat/long
        response = requests.get("{0}/Spoorkaart-API/api/v1/spoorkaart".format(os.getenv('NS_API_BASE_URL')),
                                headers={
                                    "Cache-Control": "no-cache",
                                    "Ocp-Apim-Subscription-Key": os.getenv('NS_API_KEY')
                                })
        # Parse JSON content
        rail_routes_data = response.json()

        def random_color_generator():
            color = np.random.randint(0, 256, size=3)
            return tuple(color)

        cleaned_rail_routes_data = []
        # Loop over all results in the retrieved data to select only necessary attributes
        for route in rail_routes_data['payload']['features']:
            route['style'] = {'color': 'rgb{0}'.format(random_color_generator())}
            cleaned_rail_routes_data.append(route)

        return json.dumps(cleaned_rail_routes_data)

    except requests.exceptions.HTTPError as http_err:
        abort(404, 'HTTP Error: 404 {}'.format(http_err.response.text))


@rail_routes_blueprint.route("/rail_routes/lines")
def get_rail_routes_lines():
    return json.dumps([
        {
            "id": "1",
            "name": "Zaandam – Schiphol "
        },
        {
            "id": "2",
            "name": "Hoorn – Zaandam "
        },
        {
            "id": "3",
            "name": "Amsterdam Centraal – Hilversum "
        },
        {
            "id": "4",
            "name": "Tilburg – ’s Hertogenbosch "
        },
        {
            "id": "5",
            "name": "Hilversum – Schiphol "
        },
        {
            "id": "6",
            "name": "Schiphol – Almere Centrum "
        },
        {
            "id": "7",
            "name": "Amsterdam Centraal – Hoorn "
        },
        {
            "id": "8",
            "name": "Utrecht – ’s Hertogenbosch "
        },
        {
            "id": "9",
            "name": "’s Hertogenbosch – Utrecht "
        },
        {
            "id": "10",
            "name": "Zaandam – Hoorn"
        }
    ])
