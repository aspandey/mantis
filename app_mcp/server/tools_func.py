from fastapi import Request, Response
from fastapi.responses import JSONResponse
import requests
from server.app_mcp import app_mcp
from utils.app_config import get_api_key, api_key_loc


WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"

async def func_get_weather_info(city: str) -> dict:
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
    
async def func_book_flight(
    origin: str,
    destination: str,
    date: str,
    passenger_name: str
) -> dict:
    booking_id = "BOOK123456"
    return {
        "booking_id": booking_id,
        "origin": origin,
        "destination": destination,
        "date": date,
        "passenger_name": passenger_name,
        "status": "confirmed",
        "message": "Flight booked successfully."
    }

async def func_get_flight_status(
    booking_id: str
) -> dict:
    return {
        "booking_id": booking_id,
        "status": "on time",
        "departure_time": "2024-07-01T10:00:00Z",
        "arrival_time": "2024-07-01T14:00:00Z",
        "message": "Flight status fetched successfully."
}

async def func_list_flights(
    origin: str,
    destination: str,
    date: str
) -> list:
    return [
        {
            "flight_number": "FL123",
            "origin": origin,
            "destination": destination,
            "date": date,
            "departure_time": "2024-07-01T10:00:00Z",
            "arrival_time": "2024-07-01T14:00:00Z",
            "airline": "Air Dummy",
            "duration": "4 hours",
            "price": 199.99,
            "status": "available",
        },
        {
            "flight_number": "FL456",
            "origin": origin,
            "destination": destination,
            "date": date,
            "departure_time": "2024-07-01T15:00:00Z",
            "arrival_time": "2024-07-01T19:00:00Z",
            "airline": "Dummy Airlines",
            "duration": "4 hours",
            "price": 249.99,
            "status": "unavailable",
        }
    ]

async def func_cancel_flight(
    booking_id: str
) -> dict:
    return {
        "booking_id": booking_id,
        "status": "cancelled",
        "message": "Flight cancelled successfully."
    }