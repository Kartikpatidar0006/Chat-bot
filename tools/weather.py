import requests

def execute(arguments: dict):
    city = arguments.get("city")

    if not city:
        return "Weather error: city not provided"
    
    try:
        # Fetch weather in JSON format from wttr.in
        url = f"https://wttr.in/{city}"
        response = requests.get(
            url,
            params={"format": "j1"},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()

        current = data["current_condition"][0]
        temp = current.get("temp_C")
        feels_like = current.get("FeelsLikeC")
        humidity = current.get("humidity")
        windspeed = current.get("windspeedKmph")
        
        weather_desc = "Unknown"
        if current.get("weatherDesc"):
            weather_desc = current["weatherDesc"][0].get("value", "Unknown")

        # Attempt to get area/country names
        area_name = city
        country = ""
        if "nearest_area" in data and data["nearest_area"]:
            area = data["nearest_area"][0]
            if area.get("areaName"):
                area_name = area["areaName"][0].get("value", city)
            if area.get("country"):
                country = area["country"][0].get("value", "")

        country_str = f", {country}" if country else ""
        return (
            f"City: {area_name}{country_str}\n"
            f"Temperature: {temp}°C (Feels like: {feels_like}°C)\n"
            f"Condition: {weather_desc}\n"
            f"Humidity: {humidity}%\n"
            f"Wind Speed: {windspeed} km/h"
        )

    except Exception as e:
        # Fallback to plain-text format if JSON API fails or rate-limits
        try:
            url = f"https://wttr.in/{city}"
            response = requests.get(url, params={"format": 3}, timeout=10)
            response.raise_for_status()
            return response.text.strip()
        except Exception as e2:
            return f"Weather error: Could not retrieve weather for {city}. (JSON Error: {e}, Text Error: {e2})"

if __name__ == "__main__":
    print("weather tool\n")
    print(execute({"city": "delhi"}))