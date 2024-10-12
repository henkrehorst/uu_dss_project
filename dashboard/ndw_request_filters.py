import requests
import json

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

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)