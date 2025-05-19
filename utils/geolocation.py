# utils/geolocation.py

import requests

def get_coordinates(postcode):
    """
    Convert a UK postcode to latitude and longitude using Postcodes.io API.

    Parameters:
        postcode (str): UK postcode

    Returns:
        tuple: (latitude, longitude)
    """
    url = f"https://api.postcodes.io/postcodes/{postcode}"
    response = requests.get(url)

    if response.status_code == 200:
        result = response.json()["result"]
        return result["latitude"], result["longitude"]
    else:
        raise ValueError("Invalid postcode or Postcodes.io API error.")
