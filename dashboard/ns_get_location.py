import requests
import json

lat = 52.535164 # Placeholder, put in actual lat/long of location of road works
lng = 6.0996347 # Placeholder
limit = 2 #Placeholder, define limit of no. of stations you want to retrieve

# Primary Key from NS API
primary_key = "0c97e49d1a0e4a10bb2313d4bb697472"  

# Placeholder for the URL
url = f"https://gateway.apiportal.ns.nl/nsapp-stations/v3/nearest?lat={lat}&lng={lng}[&limit={limit}][&includeNonPlannableStations]"

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

# Cleaning the data so it becomes more readable and removes uneccesary information
def clean_station_data(data):
    cleaned_data = []
    # Loop over all results in the retrieved data to select only necessary attributes
    for station in data['payload']:
        cleaned_station = {
            "stationType": station.get("stationType"),
            "names": station.get("names", {}).get("long"),
            "distance": station.get("distance"),
            "location": station.get("location")
        }
        # Append to empty list to create new list with useable variables
        cleaned_data.append(cleaned_station)
    return cleaned_data

cleaned_stations_data = clean_station_data(stations_data)

print(json.dumps(cleaned_stations_data, indent=4))
