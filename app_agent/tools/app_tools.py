from typing import TypedDict, List, Annotated, Sequence
from langchain_core.tools import tool

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
from langchain_core.tools import tool, InjectedToolCallId
from langgraph.types import Command
from langgraph.graph import MessagesState
from langgraph.prebuilt import InjectedState

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

# Handoffs
transfer_to_portfolio_assistant = create_handoff_tool(
    agent_name="portfolio_assistant",
    description="Transfer user to the equity portfolio assistant.",
)
transfer_to_flight_assistant = create_handoff_tool(
    agent_name="flight_assistant",
    description="Transfer user to the flight-booking assistant.",
)

@tool
def book_hotel(hotel_name: str) -> str:
    """Book a hotel"""
    return f"Successfully booked a stay at {hotel_name}."

@tool
def cancel_hotel_booking(booking_id: str) -> str:
    """Cancel a hotel booking"""
    return f"Successfully cancelled the booking with ID {booking_id}."

@tool
def get_hotel_details(hotel_name: str) -> str:
    """Get details of a hotel"""
    return f"Details for {hotel_name}: 5-star hotel with pool, gym, and spa facilities."

# ===========================

HOTEL_TOOLS = [
    book_hotel,
    cancel_hotel_booking,
    get_hotel_details,
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

