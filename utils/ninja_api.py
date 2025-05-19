import requests
from config import RENEWABLES_NINJA_API_KEY

def get_ninja_data(lat, lon, tech="solar", year=2021):
    """
    Fetch solar or wind data from Renewables.ninja API.
    """
    base_url = f"https://www.renewables.ninja/api/data/{tech}"
    headers = {
        "Authorization": f"Token {RENEWABLES_NINJA_API_KEY}"
    }

    # Required model for each tech
    model = "pv" if tech == "solar" else "merra2"

    params = {
        "lat": lat,
        "lon": lon,
        "date_from": f"{year}-01-01",
        "date_to": f"{year}-12-31",
        "format": "json",
        "header": True,
        "tz": "Europe/London",
        "capacity": 1,
        "system_loss": 0.1,
        "model": model  # THIS IS THE CRITICAL LINE
    }

    # Optional: add height for wind
    if tech == "wind":
        params["height"] = 100

    response = requests.get(base_url, headers=headers, params=params)

    if response.status_code != 200:
        raise Exception(f"API Error {response.status_code}: {response.text}")
    
    return response.json()
