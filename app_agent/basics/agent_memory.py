from typing import TypedDict, Literal, Annotated, Sequence

from langchain_ollama import ChatOllama
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, BaseMessage, AnyMessage, RemoveMessage
from langchain_core.tools import tool

from langgraph.graph import StateGraph, END, START, MessagesState
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition

from IPython.display import display
from langgraph.checkpoint.memory import MemorySaver, InMemorySaver
from langchain_core.runnables import RunnableConfig


class AgentState(MessagesState):
    """
    State class. Instance of this class will be shared
    by different nodes to pass messages from one state to other.
    """
    pass

messages : list[AnyMessage] = [HumanMessage(content="Hello! I am Sam.", id="1")]
messages.extend([SystemMessage(content="You are a helpful assistant.", id="2")])
messages.extend([AIMessage(content="I can help you with a variety of tasks.",   id="3")])
messages.extend([HumanMessage(content="What is the capital of France?", id="4")])
messages.extend([AIMessage(content="The capital of France is Paris.", id="5")])
messages.extend([HumanMessage(content="My name is Sam. I have a question. What is the capital of France?", id="6")])

chat_llm = ChatOllama(
    model="llama3.2:latest",
    temperature=0.0
    )

def agent_call(state: AgentState) -> AgentState:
    response = chat_llm.invoke(state["messages"])
    return {"messages": state["messages"] + [AIMessage(content=response.content)]}


def delete_messages(state: AgentState)  -> AgentState:

    total = state["messages"]
    trimmed : list[AnyMessage]= []
    if len(total) > 2:
        trimmed = [RemoveMessage(id=m.id) for m in total[:-2]]
    
    return {"messages": trimmed}

memory = InMemorySaver()
config = RunnableConfig(configurable={"thread_id": "1"})

gp = StateGraph(AgentState)
gp.add_node("agent_call", agent_call)
gp.add_node("delete_messages", delete_messages)

gp.set_entry_point("agent_call")
gp.add_edge("agent_call", "delete_messages")
gp.add_edge("delete_messages", END)

app = gp.compile(checkpointer=memory)

res = app.invoke({"messages": messages}, config=config)
messages = [HumanMessage(content="What is my name?")]
res = app.invoke({"messages": messages}, config=config)

for msg in res["messages"]:
    msg.pretty_print()