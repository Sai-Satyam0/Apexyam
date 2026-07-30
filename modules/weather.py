import requests
import streamlit as st

def get_weather(city: str) -> dict:
    """Get weather data for a city using Open-Meteo API."""
    try:
        if not city or not city.strip():
            st.error("Please enter a city name")
            return None

        # Geocoding
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
        geo_response = requests.get(geo_url, timeout=10)
        geo_response.raise_for_status()
        geo_data = geo_response.json()

        if "results" not in geo_data or not geo_data["results"]:
            st.error(f"City '{city}' not found")
            return None

        lat = geo_data["results"][0]["latitude"]
        lon = geo_data["results"][0]["longitude"]
        city_name = geo_data["results"][0]["name"]

        # Weather forecast
        weather_url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}"
            f"&current=temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code"
        )
        weather_response = requests.get(weather_url, timeout=10)
        weather_response.raise_for_status()
        weather_data = weather_response.json()

        current = weather_data["current"]

        # Map weather code to condition
        code = current.get("weather_code", 0)
        condition = get_weather_condition(code)

        return {
            "temperature": current.get("temperature_2m", "N/A"),
            "humidity": current.get("relative_humidity_2m", "N/A"),
            "wind_speed": current.get("wind_speed_10m", "N/A"),
            "condition": condition,
            "city": city_name
        }

    except requests.RequestException as e:
        st.error(f"Weather API error: {str(e)}")
        return None
    except Exception as e:
        st.error(f"Weather error: {str(e)}")
        return None

def get_weather_condition(code: int) -> str:
    """Map WMO weather code to condition string."""
    conditions = {
        0: "Clear sky",
        1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
        45: "Fog", 48: "Depositing rime fog",
        51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
        56: "Light freezing drizzle", 57: "Dense freezing drizzle",
        61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
        66: "Light freezing rain", 67: "Heavy freezing rain",
        71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow",
        77: "Snow grains",
        80: "Slight rain showers", 81: "Moderate rain showers", 82: "Violent rain showers",
        85: "Slight snow showers", 86: "Heavy snow showers",
        95: "Thunderstorm", 96: "Thunderstorm with slight hail", 99: "Thunderstorm with heavy hail"
    }
    return conditions.get(code, "Unknown")

def format_response(data: dict) -> str:
    """Format weather data into natural sentence."""
    return (
        f"It's currently {data['condition'].lower()} in {data['city']} with a temperature of "
        f"{data['temperature']}°C. Humidity is at {data['humidity']}% and wind speed is "
        f"{data['wind_speed']} km/h."
    )
