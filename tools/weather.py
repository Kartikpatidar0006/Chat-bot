import requests

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

def execute(arguments: dict):
    city = arguments.get("city")

    if not city:
        return "Weather error: city not provided"
    
    try:
        geo_response = requests.get(
            GEOCODING_URL,
            params={
                "name": city,
                "count": 1
            },
            timeout=10
        )
        geo_response.raise_for_status()
        geo_data = geo_response.json()

        if "results" not in geo_data:
            return f"City not found: {city}"
        
        location = geo_data["results"][0]
        latitude = location["latitude"]
        longitude = location["longitude"]
        city_name = location["name"]
        country = location.get("country", "")

        weather_response = requests.get(
            WEATHER_URL,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current_weather": True
            },
            timeout=10
        )
        weather_response.raise_for_status()
        weather_data = weather_response.json()

        current = weather_data["current_weather"]
        temperature = current.get("temperature")
        weather_code = current.get("weathercode")
        windspeed = current.get("windspeed")

        return (
            f"City: {city_name}, {country}\n"
            f"Temperature: {temperature}°C\n"
            f"Wind Speed: {windspeed} km/h\n"
            f"Weather Code: {weather_code}"
        )

    except Exception as e:
        return f"Weather error: {e}"

if __name__ == "__main__":
    print("weather tool\n")
    print(execute({"city": "delhi"}))