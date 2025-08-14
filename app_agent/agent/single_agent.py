from typing import TypedDict, List, Annotated, Sequence, Any

from langchain_core.messages import BaseMessage
from langchain_core.messages import HumanMessage
from langchain_core.messages import SystemMessage
from langchain_ollama import ChatOllama
from langchain_core.runnables import RunnableConfig

from langgraph.graph import StateGraph, END, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
import logging as dbg
import asyncio
import utils.agent_config as app_config
from langchain.tools import StructuredTool as LCTool

from mcp_client.mcp_client import APP_MCPTools
import tools.app_tools as app_tools
import utils.agent_utils as agent_utils
dbg = app_config.DEBUG_APP

GENERATIVE_MODEL = app_config.GENERATIVE_MODEL
servers = [*app_config.MCP_SERVERS.values()]

# This is the agent which will use tools from different places
# 1 - app_tools are the local tools. It means we do not need to go over the http request to get the tools.
# 2 - An Agent needs tools, prompts and resources to perform and complete the task given by user.
# These tools can be local or remote. Remote means, provided by MCP server.

async def get_mcp_tools(servers: List[str]) -> List[LCTool]:
    mcp_tools = await APP_MCPTools.create(servers)
    return mcp_tools.tools

tools = asyncio.run(get_mcp_tools(servers))
tools = tools + app_tools.APP_TOOLS
dbg.info(f"\nAPP tools = {app_tools.APP_TOOLS} \n\n")
dbg.info(f"\nMCP tools = {tools} \n\n")

# Bind tools to the model which will handle user queries and tool calls.
llm = ChatOllama(
    model=GENERATIVE_MODEL,
    temperature=0 ,
).bind_tools(tools)

class AgentState(TypedDict):
    """
    State class. Instance of this class will be shared
    by different nodes to pass messages from one state to other.
    """
    messages: Annotated[Sequence[BaseMessage], add_messages]

async def app_agent_invoke_model(state: AgentState) -> AgentState:
    """
    A function which will act as Agent and will be used on a node.
    Node will be called as agent node.
    """
    state_message = state["messages"]
    dbg.info(f"Received State Message: {state_message}\n")
    system_prompt = SystemMessage(
            content="You are a helpful assistant. Answer the user queries to the best of your ability. \
            You may call tools to answer the queries. Reply in natural language."
        )
    response = await llm.ainvoke([system_prompt, *state_message])
    dbg.info(f"Response State Message: {response}\n")
    return {"messages": [response]}

def check_for_tools_call(state: AgentState) -> str:
    """ A function which will be used on a node to check if the conversation should continue."""
    messages = state["messages"]
    last_message = messages[-1].model_dump()
    if not last_message["tool_calls"]:
        dbg.info(f"No tool calls found in the last message.\n")
        return "end"
    else:
        dbg.info(f"Tool calls found in the last message.\n {last_message["tool_calls"]}")
        return "continue"


# *** Create graph by creating nodes and edges connecting those nodes. ***
def create_and_compile_graph():
    """
    Creates and compiles a state graph for an agent workflow.
    Returns:
        app: The compiled application representing the agent's workflow state graph.
    """
    graph = StateGraph(AgentState)
    memory = MemorySaver()

    tools_node_functions = ToolNode(tools=tools)
    graph.add_node("agent_node", app_agent_invoke_model)
    graph.add_node("tools_node", tools_node_functions)

    graph.set_entry_point("agent_node")

    graph.add_conditional_edges(
        "agent_node",
        check_for_tools_call,
        {
            "continue": "tools_node",
            "end": END,
        },
    )
    graph.add_edge("tools_node", "agent_node")
    graph.add_edge("agent_node", END)

    app = graph.compile(checkpointer=memory)
    return app

def display_graph():
    """ Function to display the graph in a readable format. """
    print(app.get_graph().draw_ascii())

app = create_and_compile_graph()
# display_graph()

config = RunnableConfig(configurable={"thread_id": "1"})

async def main():
    print("Welcome!! I am Tigress, Your Agent.")
    print(f"Type 'bye' to quit.")
    while True:
        user_input = input(f"You : ")
        if user_input.strip().lower() == "bye":
            print("Goodbye!")
            dbg.info(f"No more request, going to end node\n")
            break
        input_state = {"messages": [HumanMessage(content=user_input)]}
        results = [item async for item in app.astream(input_state, stream_mode="values", config=config)]
        agent_utils.print_state_messages(results)

if __name__ == "__main__":
    asyncio.run(main())


# Run agent as module from parent directory which contains all other modules.
# p3 -m agent.agent



