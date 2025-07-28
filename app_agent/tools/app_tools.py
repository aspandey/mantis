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

@tool
def calculate_xirr(cashflows: List[float]) -> float:
    """ A function which will be used as a tool to calculate XIRR."""
    return 10.0

APP_TOOLS = [
        introduction,
        compound_interest,
        time_to_double_investment,
        calculate_xirr,
        add_number,
        multiply_number,
        subtract_number,
        greet_user
    ]

