import requests

def fetch_weather(street, city, state, zip):
    try:
        # Geolocation API for coordinates
        street = street.replace(" ","+")
        geo_api_url = f"https://geocoding.geo.census.gov/geocoder/locations/onelineaddress?address={street}%2C+{city}%2C+{state}+{zip}&benchmark=4&format=json"
        geo_response = requests.get(geo_api_url).json()

        # Ensure valid response from the geocoding API
        address_matches = geo_response.get("result", {}).get("addressMatches", [])
        if not address_matches:
            return f"Error: Unable to find location for {city}, {state}. Please check the spelling or try another location."

        coordinates = address_matches[0]["coordinates"]

        # Get grid points for NWS
        lat, lon = coordinates["y"], coordinates["x"]
        grid_url = f"https://api.weather.gov/points/{lat},{lon}"
        grid_response = requests.get(grid_url).json()

        # Ensure valid grid response
        if "properties" not in grid_response:
            return "Error: Unable to fetch grid data from NWS API."

        forecast_url = grid_response["properties"]["forecast"]

        # Fetch weather forecast
        forecast_response = requests.get(forecast_url).json()
        if "properties" not in forecast_response or "periods" not in forecast_response["properties"]:
            return "Error: Unable to fetch forecast data from NWS API."

        periods = forecast_response["properties"]["periods"]

        return periods
    except Exception as oops:
        return f"Error: {oops}"
