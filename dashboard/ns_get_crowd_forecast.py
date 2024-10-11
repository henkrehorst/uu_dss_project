import requests
import json

ritnummer = 654 # Placeholder

# Primary Key from NS API
primary_key = "0c97e49d1a0e4a10bb2313d4bb697472"  

# Placeholder for the URL
url = f"https://gateway.apiportal.ns.nl/virtual-train-api/v1/prognose/{ritnummer}"

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
    crowd_forecast = response.json()

except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")  # e.g., 404 Not Found

print(json.dumps(crowd_forecast, indent=4))

'''
This code outputs the classification (either LOW, MEDIUM or HIGH) per stationUic (unique station code).
However, there is  no logical order in the JSON output.
'''
