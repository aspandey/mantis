from typing import TypedDict, Literal, Annotated, Sequence
from random import random
from langgraph.graph import StateGraph, END
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, AnyMessage
from langgraph.graph.message import add_messages

message : list[AnyMessage]
message = [AIMessage(content="Hello from AI")]
message.extend([HumanMessage(content="Hello from Human")])
message.extend([SystemMessage(content="Hello from System")])
for msg in message:
    msg.pretty_print()