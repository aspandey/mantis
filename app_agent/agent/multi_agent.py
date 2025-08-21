from typing import TypedDict, List, Annotated, Sequence
import logging as dbg
import asyncio

from langchain_core.messages import AnyMessage, HumanMessage, SystemMessage
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, END, START, MessagesState
from langgraph.graph.message import add_messages
from langgraph.prebuilt import create_react_agent
from langchain.tools import StructuredTool as LCTool
from langchain_core.runnables import RunnableConfig

from mcp_client.mcp_client import APP_MCPTools
import tools.app_tools as app_tools
import utils.agent_config as app_config
import utils.agent_utils as agent_utils

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph

checkpointer = InMemorySaver()

dbg = app_config.DEBUG_APP
GENERATIVE_MODEL = app_config.GENERATIVE_MODEL

async def get_mcp_tools(servers: List[str]) -> List[LCTool]:
    mcp_tools = await APP_MCPTools.create(servers)
    return mcp_tools.tools

flight_tools = asyncio.run(get_mcp_tools([app_config.MCP_SERVERS["flight"]]))
flight_tools = [app_tools.transfer_to_portfolio_assistant] + flight_tools

kite_tools = asyncio.run(get_mcp_tools([app_config.MCP_SERVERS["kite"]]))
kite_tools = [app_tools.transfer_to_flight_assistant] + kite_tools

llm = ChatOllama(
    model=GENERATIVE_MODEL,
    temperature=0 ,
)

# Define agents
flight_assistant = create_react_agent(
    model=llm,
    tools=flight_tools,
    prompt="You are a flight booking assistant",
    name="flight_assistant",
)

# hotel_assistant = create_react_agent(
portfolio_assistant = create_react_agent(
    model=llm,
    tools=app_tools.HOTEL_TOOLS,
    prompt="You are a hotel booking assistant",
    name="hotel_assistant",
)

# Define multi-agent graph
multi_agent_graph = (
    StateGraph(MessagesState)
    .add_node(flight_assistant)
    .add_node(portfolio_assistant)
    .add_edge(START, "flight_assistant")
    .compile(checkpointer=checkpointer)
)

class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

sys_msg = SystemMessage(
    content="You are a multi-agent system. You can transfer the user to different agents based on their requests. \
    You can also book flights and hotels."
)
hum_msg = HumanMessage(
    content="Book a flight from BOS to JFK. Also book my stay at the hotel TAJ."
)
input_state = {"messages": [hum_msg]}

config = RunnableConfig(configurable={"thread_id": "1"})

async def main():
    print("Welcome!! I am Your Agent.")
    print(f"Type 'bye' to quit.")
    while True:
        user_input = input(f"You : ")
        if user_input.strip().lower() == "bye":
            print("Goodbye!")
            dbg.info(f"No more request, going to end node\n")
            break
        input_state = {"messages": [HumanMessage(content=user_input)]}
        results = [item async for item in multi_agent_graph.astream(input_state, stream_mode="values", config=config)]
        agent_utils.print_state_messages(results)

if __name__ == "__main__":
    asyncio.run(main())

# Run agent as module from parent directory which contains all other modules.
# p3 -m agent.multi_agent

