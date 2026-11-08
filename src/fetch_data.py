import time
from datetime import date, timedelta
from pathlib import Path

import pandas as pd
import requests
from config import NASA_API_KEY

url = "https://api.nasa.gov/neo/rest/v1/feed"
records = []

end = date(2026, 11, 7)

for week in range(30):
    start = end - timedelta(days=6)
    params = {
        "start_date": start.isoformat(),
        "end_date": end.isoformat(),
        "api_key": NASA_API_KEY,
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        print("Problem with", start, "to", end, "- status:", response.status_code)
        break

    data = response.json()
    for day, asteroids in data["near_earth_objects"].items():
        for asteroid in asteroids:
            approach = asteroid["close_approach_data"][0]
            records.append({
                "name": asteroid["name"],
                "date": day,
                "diameter_min_m": asteroid["estimated_diameter"]["meters"]["estimated_diameter_min"],
                "diameter_max_m": asteroid["estimated_diameter"]["meters"]["estimated_diameter_max"],
                "velocity_kmps": float(approach["relative_velocity"]["kilometers_per_second"]),
                "miss_distance_km": float(approach["miss_distance"]["kilometers"]),
                "hazardous": asteroid["is_potentially_hazardous_asteroid"],
            })

    print("Fetched", start, "to", end, "- total so far:", len(records))
    end = start - timedelta(days=1)
    time.sleep(1)

df = pd.DataFrame(records).drop_duplicates()

print("Table shape (rows, columns):", df.shape)
print(df["hazardous"].value_counts())

save_path = Path(__file__).resolve().parent.parent / "data" / "asteroids.csv"
df.to_csv(save_path, index=False)
print("Saved to:", save_path)