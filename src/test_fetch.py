import requests
from config import NASA_API_KEY

url = "https://api.nasa.gov/neo/rest/v1/feed"
params = {
    "start_date": "2026-11-01",
    "end_date": "2026-11-07",
    "api_key": NASA_API_KEY,
}

response = requests.get(url, params=params)
print("Status code:", response.status_code)
print("Asteroids found:", response.json()["element_count"])
data = response.json()
first_day = list(data["near_earth_objects"].keys())[0]
first_asteroid = data["near_earth_objects"][first_day][0]

print("Name:", first_asteroid["name"])
print("Hazardous:", first_asteroid["is_potentially_hazardous_asteroid"])
print("Max size (m):", first_asteroid["estimated_diameter"]
                        ["meters"]["estimated_diameter_max"])
print("Miss distance (km):", first_asteroid["close_approach_data"]
                        [0]["miss_distance"]["kilometers"])