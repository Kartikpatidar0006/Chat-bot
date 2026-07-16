import requests

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

WMO_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Slight snow fall",
    73: "Moderate snow fall",
    75: "Heavy snow fall",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail"
}

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

        condition = WMO_CODES.get(weather_code, f"Code {weather_code}")

        country_str = f", {country}" if country else ""
        return (
            f"City: {city_name}{country_str}\n"
            f"Temperature: {temperature}°C\n"
            f"Condition: {condition}\n"
            f"Wind Speed: {windspeed} km/h"
        )

    except Exception as e:
        return f"Weather error: {e}"

if __name__ == "__main__":
    print("weather tool\n")
    print(execute({"city": "delhi"}))