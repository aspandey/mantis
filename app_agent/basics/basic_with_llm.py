from typing import TypedDict, Literal
from random import random
from langgraph.graph import StateGraph, END

class GraphState(TypedDict):
    messages: str

def node_1(state: GraphState) -> GraphState:
    return {"messages": state['messages'] + "hello from Node 1"}

def node_2(state: GraphState) -> GraphState:
    return {"messages": state['messages'] + "hello from Node 2"}

def node_3(state: GraphState) -> GraphState:
    return {"messages": state['messages'] + "hello from Node 3"}

def decide_node(state: GraphState) -> Literal["node_2", "node_3"]:
    if random() < 0.5:
        return "node_2"
    else:
        return "node_3"

gb = StateGraph(GraphState)
gb.add_node("node_1", node_1)
gb.add_node("node_2", node_2)
gb.add_node("node_3", node_3)

gb.add_conditional_edges("node_1", decide_node)
gb.add_edge("node_2", END)
gb.add_edge("node_3", END)
gb.set_entry_point("node_1")
app = gb.compile()
content : GraphState = {"messages": "start-"}

message = app.invoke(content)
print(message)
