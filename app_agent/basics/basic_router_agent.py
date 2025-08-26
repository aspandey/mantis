from typing import TypedDict, Literal, Annotated, Sequence

from langchain_ollama import ChatOllama
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, AnyMessage, BaseMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition
from IPython.display import display


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

@tool
def multiply_numbers(a: int, b:int) -> int:
    """ Multiplies two numbers and returns the results"""
    return a * b
    
tools = [multiply_numbers]

chat_llm = ChatOllama(
    model="llama3.2:latest",
    temperature=0
).bind_tools(tools) # After few hours of debugging , I found that we need to bind the tools at the time of creating CHatOllama

def call_llm(state: AgentState) -> AgentState:
    system_prompt = SystemMessage(content="You are a helpful assistant with access to tools. \
                    If a tool is relevant, ALWAYS call it instead of answering directly. \
                    Return only valid JSON tool calls when using tools."
                    )
    state_message = state["messages"]
    res = chat_llm.invoke([system_prompt, *state_message])
    return {"messages": [res]}

def check_for_tools_call(state: AgentState) -> str:
    """ A function which will be used on a node to check if the conversation should continue."""
    messages = state["messages"]
    last_message = messages[-1].model_dump()
    if not last_message["tool_calls"]:
        return "end"
    else:
        return "continue"
    
tools_node_functions = ToolNode(tools=tools)
gp = StateGraph(AgentState)
gp.add_node("call_llm", call_llm)
gp.add_node("tools", tools_node_functions )

gp.add_edge(START, "call_llm")
gp.add_conditional_edges(
        "call_llm",
        check_for_tools_call,
        {
            "continue": "tools",
            "end": END,
        },
    )
gp.add_edge("tools", "call_llm")
app = gp.compile()
# display(app.get_graph().draw_ascii())

mesg : AgentState = {"messages" : [HumanMessage(content="Multiply two numbers 2 and 6")]}
# mesg : AgentState = {"messages" : [HumanMessage(content="PLease book a hotel")]}
res = app.invoke(mesg)
# results = [item for item in app.stream(mesg, stream_mode="values")]


for msg in res["messages"]:
    msg.pretty_print()
