import requests
import json

lat = 52.535164 # Placeholder, put in actual lat/long of location of road works
lng = 6.0996347 # Placeholder
limit = 2

# Placeholder for the URL
url = f"https://gateway.apiportal.ns.nl/nsapp-stations/v3/nearest?lat={lat}&lng={lng}[&limit={limit}][&includeNonPlannableStations]"
# Primary Key from NS API
primary_key = "0c97e49d1a0e4a10bb2313d4bb697472"  

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
    data = response.json()
    # Pretty print JSON data
    print(json.dumps(data, indent=4))

except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")  # e.g., 404 Not Found