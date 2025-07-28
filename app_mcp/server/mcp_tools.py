from fastapi import Request, Response
from fastapi.responses import JSONResponse
import requests
import os
from server.app_mcp import app_mcp
from utils.app_config import get_api_key, api_key_loc


WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"

@app_mcp.tool(
    name="get_weather_info",
    description="Fetches current weather information for a given city in the world.",
    tags={"weather", "city", "forecast"}
)
async def get_weather_info(city: str) -> dict:
    """
    Fetches current weather information for the specified city using the OpenWeatherMap API.
    Returns a dictionary with temperature, weather description, humidity, and wind speed.
    """
    # Read API key from file
    api_key = get_api_key(api_key_loc, "WEATHER_API_KEY")
    req_params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }
    try:
        resp = requests.get(WEATHER_URL, params=req_params, timeout=20)
        if resp.status_code != 200:
            return {"error": f"Failed to fetch weather data: {resp.json().get('message', 'Unknown error')}"}
        data = resp.json()
        weather_info = {
            "city": data.get("name"),
            "country": data.get("sys", {}).get("country"),
            "temperature_celsius": data.get("main", {}).get("temp"),
            "weather": data.get("weather", [{}])[0].get("description"),
            "humidity": data.get("main", {}).get("humidity"),
            "wind_speed_mps": data.get("wind", {}).get("speed")
        }
        return weather_info
    except Exception as e:
        return {"error": str(e)}

@app_mcp.tool(
    name="greet_person",
    description="Say hello to person by name.",
    tags={"greet", "hello"}
)
def greet(name: str) -> str:
    """Greets the user by name."""
    return f"Helloooooooooooooo, {name}!"

@app_mcp.tool(
    name="simple_interest",
    description="Given principal, rate and time, calculate simple interest.",
    tags={"simple", "interest"}
)
def simple_interest(principal: float, rate: float, time: int) -> float:
    """A function which will be used as a tool to calculate simple interest."""
    return (principal * rate * time) / 100

