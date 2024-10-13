import requests
import json

#created a function to encapsulate all the code
def get_roadwork_data():
  url = "https://melvin.ndw.nu/melvinservice/rest/public/all"

  payload = json.dumps({
    "filter": {
      "dateFrom": "2024-10-11",
      "dateTill": "2024-10-18",
      "situationTypes": [
          "ROADWORKS"
          ],
      "situationVehicleTypes": [
          "CARS"
          ],
      "project": [],
      "statuses": [
          "PLANNED", 
          "ONGOING", 
          "COMPLETED"
          ],
      "periodStatuses": [
          "ACTIVE",
          "PLANNED"
          ],
      "delays": [
          "NO_DELAY",
          "MINOR", 
          "MAJOR"
          ],
      "impacts": [
        "LITTLE",
        "AVERAGE",
        "BIG",
        "HUGE"
      ],
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
    response = response = requests.request("POST", url, headers=headers, data=payload)
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

get_roadwork_data()
