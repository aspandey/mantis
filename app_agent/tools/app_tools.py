from typing import TypedDict, List, Annotated, Sequence

from langchain_core.tools import tool, InjectedToolCallId
from langgraph.types import Command
from langgraph.graph import MessagesState
from langgraph.prebuilt import InjectedState
import uuid
from datetime import datetime, timedelta
from utils.agent_config import DEBUG_APP as dbg

@tool
def introduction() -> str:
    """
    A function which can help you solve some basic maths problems.
    """
    message = """ I am courtesious Maths tool. I can help you solve some basic maths problems!!"""
    return message

@tool
def add_number (a: int , b: int) -> int:
    """ A function which will be used as a tool to add two numbers."""
    return a + b

@tool
def multiply_number (a: int , b: int) -> int:
    """ A function which will be used as a tool to multiply two numbers."""
    return a * b

@tool
def subtract_number (a: int , b: int) -> int:
    """ A function which will be used as a tool to subtract b from a."""
    
    return a - b

@tool
def greet_user(name: str = "Tom") -> str:
    """ A function which will be used as a tool to greet the user."""
    return f"Hello, {name}!"

@tool
def compound_interest(principal: float, rate: float, time: int) -> float:
    """ A function which will be used as a tool to calculate compound interest."""
    return (principal * (1 + rate) ** time) + principal

@tool
def time_to_double_investment(principal: float, rate: float) -> float:
    """ A function which will be used as a tool to calculate time, in years, to double investment."""
    return 72 / rate

# ============================
def create_handoff_tool(*, agent_name: str, description: str | None = None):
    name = f"transfer_to_{agent_name}"
    description = description or f"Transfer to {agent_name}"

    @tool(name, description=description)
    async def handoff_tool(state: Annotated[MessagesState, InjectedState], tool_call_id: Annotated[str, InjectedToolCallId],) -> Command:
        tool_message = {
            "role": "tool",
            "content": f"Successfully transferred to {agent_name}",
            "name": name,
            "tool_call_id": tool_call_id,
        }
        return Command(  
            goto=agent_name,  
            update={"messages": state["messages"] + [tool_message]},  
            graph=Command.PARENT,  
        )
    return handoff_tool

transfer_to_portfolio_assistant = create_handoff_tool(
    agent_name="portfolio_assistant",
    description="Transfer user to the kite equity portfolio assistant.",
)
transfer_to_flight_assistant = create_handoff_tool(
    agent_name="flight_assistant",
    description="Transfer user to the flight-booking assistant. If a User is asking anything related to flight, transfer them to the flight assistant.",
)

transfer_to_hotel_assistant = create_handoff_tool(
    agent_name="hotel_assistant",
    description="Transfer user to the Hotel-booking assistant. If a User is asking anything related to hotel, transfer them to the hotel assistant.",
)

@tool
def book_hotel(
    hotel_name: str,
    guest_name: str,
    check_in_date: str,
    check_out_date: str,
    price: float = 299.99
) -> str:
    """Book a stay for the guest in a hotel"""
    booking_id = str(uuid.uuid4())

    # Provide defaults if not supplied
    if not hotel_name:
        hotel_name = "Hotel Sunshine"
    if not guest_name:
        guest_name = "Guest"
    if not check_in_date:
        check_in_date = datetime.now().strftime("%Y-%m-%d")
    if not check_out_date:
        check_out_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    if not price:
        price = 299.99

    booking_details = (
        f"Booking Details:\n"
        f"Hotel: {hotel_name}\n"
        f"Guest: {guest_name}\n"
        f"Check-in: {check_in_date}\n"
        f"Check-out: {check_out_date}\n"
        f"Booking ID: {booking_id}\n"
        f"Total Price: ${price}\n"
    )

    print(booking_details)
    return f"Successfully booked a stay at {booking_details}."

@tool
def cancel_hotel_booking(hotel_name: str, guest_name: str, booking_id: str) -> str:
    """Cancel a hotel booking and return the canceled booking details"""
    canceled_details = (
        f"Canceled Booking Details:\n"
        f"Hotel: {hotel_name}\n"
        f"Guest: {guest_name}\n"
        f"Booking ID: {booking_id}\n"
        f"Status: Cancelled\n"
    )
    print(canceled_details)
    return f"Successfully cancelled the booking.\n{canceled_details}"

@tool
def get_hotels_in_city(city: str) -> List[dict]:
    """
    Get a list of hotels in a given city along with some features.
    """
    hotels = [
        {
            "name": "Hotel Sunshine",
            "features": ["Free WiFi", "Pool", "Breakfast included", "Gym"],
            "city": city,
        },
        {
            "name": "Grand Plaza",
            "features": ["Spa", "Restaurant", "Airport Shuttle", "Pet Friendly"],
            "city": city,
        },
        {
            "name": "Ocean View Resort",
            "features": ["Beachfront", "Bar", "Kids Club", "Free Parking"],
            "city": city,
        },
        {
            "name": "Mountain Retreat",
            "features": ["Mountain View", "Hiking Trails", "Fireplace", "Sauna"],
            "city": city,
        },
    ]
    return hotels

HOTEL_TOOLS = [
    book_hotel,
    cancel_hotel_booking,
    get_hotels_in_city,
]

APP_TOOLS = [
        introduction,
        compound_interest,
        time_to_double_investment,
        add_number,
        multiply_number,
        subtract_number,
        greet_user
    ]

