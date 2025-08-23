from typing import Annotated
from langchain_core.tools import tool, InjectedToolCallId
from langgraph.prebuilt import create_react_agent, InjectedState
from langgraph.graph import StateGraph, START, MessagesState
from langgraph.types import Command
from langchain_core.messages import AnyMessage, HumanMessage, SystemMessage
import utils.agent_utils as agent_utils
from langchain.tools import StructuredTool as LCTool

# def create_handoff_tool(*, agent_name: str, description: str | None = None):
#     name = f"transfer_to_{agent_name}"
#     description = description or f"Transfer to {agent_name}"

#     @tool(name, description=description)
#     def handoff_tool(
#         state: Annotated[MessagesState, InjectedState],
#         tool_call_id: Annotated[str, InjectedToolCallId],
#     ) -> Command:
#         tool_message = {
#             "role": "tool",
#             "content": f"Successfully transferred to {agent_name}",
#             "name": name,
#             "tool_call_id": tool_call_id,
#         }
#         return Command(  
#             goto=agent_name,
#             update={"messages": state["messages"] + [tool_message]},
#             graph=Command.PARENT,
#         )
#     return handoff_tool

# Handoffs


@tool
def transfer_to_hotel_assistant(
        state: Annotated[MessagesState, InjectedState],
        tool_call_id: Annotated[str, InjectedToolCallId],
    ) -> Command:
    """Transfer user to the hotel-booking assistant."""

    tool_message = {
        "role": "tool",
        "content": f"Successfully transferred to hotel_assistant",
        "name": "transfer_to_hotel_assistant",
        "tool_call_id": tool_call_id,
    }
    return Command(  
        goto="hotel_assistant",
        update={"messages": state["messages"] + [tool_message]},
        graph=Command.PARENT,
    )


@tool
def transfer_to_flight_assistant(
        state: Annotated[MessagesState, InjectedState],
        tool_call_id: Annotated[str, InjectedToolCallId],
    ) -> Command:
    """Transfer user to the flight-booking assistant."""
    tool_message = {
        "role": "tool",
        "content": f"Successfully transferred to flight_assistant",
        "name": "transfer_to_flight_assistant",
        "tool_call_id": tool_call_id,
    }
    return Command(  
        goto="flight_assistant",
        update={"messages": state["messages"] + [tool_message]},
        graph=Command.PARENT,
    )

# transfer_to_hotel_assistant = create_handoff_tool(
#     agent_name="hotel_assistant",
#     description="Transfer user to the hotel-booking assistant.",
# )
# transfer_to_flight_assistant = create_handoff_tool(
#     agent_name="flight_assistant",
#     description="Transfer user to the flight-booking assistant.",
# )

# trns_hotel_assistent = LCTool.from_function(
#             name=tool.name,
#             description=getattr(tool, "description", "MCP tool"),
#             func=tool_func,
#             args_schema=ArgsSchema,
#             coroutine=tool_func,
#         )

# Simple agent tools
@tool
def book_hotel(hotel_name: str):
    """Book a hotel"""
    return f"Successfully booked a stay at {hotel_name}."

@tool
def book_flight(from_airport: str, to_airport: str):
    """Book a flight"""
    return f"Successfully booked a flight from {from_airport} to {to_airport}."

from langchain_ollama import ChatOllama
import utils.agent_config as app_config
GENERATIVE_MODEL = app_config.GENERATIVE_MODEL

llm = ChatOllama(
    model=GENERATIVE_MODEL,
    temperature=0 ,
)

flight_assistant = create_react_agent(
    model=llm,
    tools=[book_flight, transfer_to_hotel_assistant],
    prompt="You are a flight booking assistant. If a User is asking anything related to flight, assist them. INcase User asks anything related to hotel, transfer them to the hotel assistant." \
    "transfer user to hotel booking assitent.",
    name="flight_assistant"
)
hotel_assistant = create_react_agent(
    model=llm,
    tools=[book_hotel, transfer_to_flight_assistant],
    prompt="You are a hotel booking assistant. If a User is asking anything related to hotel, assist them. INcase User asks anything related to flight, transfer them to the flight assistant." \
    "transfer user to flight booking assitent.",
    name="hotel_assistant"
)

# Define multi-agent graph
multi_agent_graph = (
    StateGraph(MessagesState)
    .add_node(flight_assistant)
    .add_node(hotel_assistant)
    .add_edge(START, "flight_assistant")
    .compile()
)

user_input = "Book a flight from BOS to JFK. ONce it is done transfer to hotel assistent to book a hotel stay at McKittrick Hotel"
input_state = {"messages": [HumanMessage(content=user_input)]}
# Run the multi-agent graph

# results = [item for item in multi_agent_graph.stream(input_state)]
# agent_utils.print_state_messages(results)


for chunk in multi_agent_graph.stream(input_state ):
    print("=============\n")
    print(chunk)
    print("=============\n")
