import requests
import json

# Primary Key from NS API
primary_key = "0c97e49d1a0e4a10bb2313d4bb697472"

# Placeholder for the URL
url = "https://gateway.apiportal.ns.nl/Spoorkaart-API/api/v1/spoorkaart"

# Headers as defined in NS API documentation
headers = {
    "Cache-Control": "no-cache",
    "Ocp-Apim-Subscription-Key": primary_key
}
# Send GET request
try:
    # Returns JSON file with nearest train station(s) of the put in lat/long
    response = requests.get(url, headers=headers)
    # Parse JSON content
    stations_data = response.json()

except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")  # e.g., 404 Not Found

import numpy as np
def random_color_generator():
    color = np.random.randint(0, 256, size=3)
    return tuple(color)

# Cleaning the data so it becomes more readable and removes uneccesary information
def clean_station_data(data):
    cleaned_data = []
    # Loop over all results in the retrieved data to select only necessary attributes
    for route in data['payload']['features']:
        route['style']={'fill': 'rgb{0}'.format(random_color_generator()) }
        cleaned_data.append(route)


    return cleaned_data

cleaned_stations_data = clean_station_data(stations_data)

print(json.dumps(cleaned_stations_data, indent=4))
