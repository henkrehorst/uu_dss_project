import requests
import json
import pandas as pd
from sqlalchemy import create_engine
import psycopg2

lat = 52.535164 # Placeholder, put in actual lat/long of location of road works
lng = 6.0996347 # Placeholder
limit = 5 #Placeholder, define limit of no. of stations you want to retrieve

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
        location = station.get("location", {})
        lat = location.get("lat")
        lng = location.get("lng")
        
        cleaned_station = {
            "Station Type": station.get("stationType"),
            "Name": station.get("names", {}).get("long"),
            "Distance (meters)": station.get("distance"),
            "Latitude": lat, 
            "Longitude": lng   
        }
        # Append to empty list to create new list with useable variables
        cleaned_data.append(cleaned_station)
    return cleaned_data

cleaned_stations_data = clean_station_data(stations_data)

print(json.dumps(cleaned_stations_data, indent=4))

def load_to_db():
    # Create dataframe out of retrieved and cleaned data
    df_stations = pd.DataFrame(cleaned_stations_data)

    # Set up a connection to PostgreSQL with sqlalchemy
    # Note: this db connection is based on the settings on my laptop
    engine = create_engine('postgresql://student:infomdss@127.0.0.1:5434/dashboard')

    # Write the df_stations to an SQL table
    df_stations.to_sql('nearest_stations', engine, if_exists='replace', index=False)

    # Read and query the db to retrieve the table
    stations_table = pd.read_sql('SELECT * FROM nearest_stations', engine)

    # Display the data
    print(stations_table)

load_to_db()