import requests
import json
import pandas as pd
from sqlalchemy import create_engine

def get_roadwork_data():
  url = "https://melvin.ndw.nu/melvinservice/rest/public/all"

  payload = json.dumps({
    "filter": {
      "dateFrom": "2024-10-11",
      "dateTill": "2024-10-18",
      "situationTypes": [],
      "situationVehicleTypes": [],
      "project": [],
      "statuses": [],
      "periodStatuses": [];
      "delays": [],
      "impacts": [],
      "roadAuthorities": [],
      "restrictionTypes": [],
      "emergencyServicesAllowed": [],
      "publicTransportAllowed": [],
      "areaIds": [],
      "source": [],
      "conflicts": []
    }
  })
  
  headers = {
    'Content-Type': 'application/json'
  }
  
  try:
    response = requests.request("POST", url, headers=headers, data=payload)
    response.raise_for_status()
  
    roadwork_data = response.json()
    print(json.dumps(roadwork_data, indent=4))
    return roadwork_data
  
  except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
  except requests.exceptions.ConnectionError as conn_err:
    print(f"Connection error occurred: {conn_err}")
  except requests.exceptions.RequestException as req_err:
    print(f"An error occurred: {req_err}")

def load_to_db():
    engine = create_engine('postgresql://127.0.0.1:5432/dashboard')
    roadwork_data = get_roadwork_data()

    if roadwork_data:  # Check if roadwork_data is not None
        df_roadworks = pd.json_normalize(roadwork_data)  # Flatten the JSON structure if needed
        df_roadworks.to_sql('roadworks', engine, if_exists='replace', index=False)
        print("Data loaded successfully into the database.")
    else:
        print("No data to load.")

load_to_db()
