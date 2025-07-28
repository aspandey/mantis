from fastapi import Request, Response
from fastapi.responses import JSONResponse
import requests
from server.app_mcp import app_mcp
from utils.app_config import get_api_key, api_key_loc
from server.tools_func import *

WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"

@app_mcp.tool(
    name="get_weather_info",
    description="Current weather information for a given city in the world.",
    tags={"weather", "city", "forecast"}
)
async def get_weather_info(city: str) -> dict:
    """
    Fetches current weather information for the specified city using the OpenWeatherMap API.
    Returns a dictionary with tempersature, weather description, humidity, and wind speed.
    """
    return await func_get_weather_info(city)

@app_mcp.tool(
    name="book_flight",
    description="Book a flight from origin to destination on a specified date.",
    tags={"flight", "booking", "travel"}
)
async def book_flight(
    origin: str,
    destination: str,
    date: str,
    passenger_name: str
) -> dict:
    """
    Books a flight from the origin to the destination on the specified date for the given passenger.
    Returns a dictionary with booking details.
    """
    return await func_book_flight(origin, destination, date, passenger_name)

@app_mcp.tool(
    name="get_flight_status",
    description="Get the status of a flight using the booking ID.",
    tags={"flight", "status", "booking"}
)
async def get_flight_status(
    booking_id: str
) -> dict:
    """
    Retrieves the status of a flight using the provided booking ID.
    Returns a dictionary with flight status details.
    """
    return await func_get_flight_status(booking_id)

@app_mcp.tool(
    name="cancel_flight",
    description="Cancel a flight booking using the booking ID.",
    tags={"flight", "cancel", "booking"}
)
async def cancel_flight(
    booking_id: str
) -> dict:
    """
    Cancels a flight booking using the provided booking ID.
    Returns a dictionary with cancellation confirmation.
    """
    return await func_cancel_flight(booking_id)

@app_mcp.tool(
    name="list_flights",
    description="List available flights from origin to destination on a specified date.",
    tags={"flight", "list", "travel"}
)
async def list_flights(
    origin: str,
    destination: str,
    date: str
) -> list:
    """
    Lists available flights from the origin to the destination on the specified date.
    Returns a list of dictionaries with flight details.
    """
    return await func_list_flights(origin, destination, date)