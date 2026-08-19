from dotenv import load_dotenv
import os
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, ToolMessage
from operator import add as add_messages
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
from langchain_google_genai import ChatGoogleGenerativeAI

from src.tools import all_tools

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

tools = [all_tools]

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash").bind_tools(tools)

def chatbot_node(state:AgentState) -> AgentState:
    return {"messages": [llm.invoke(state["messages"])]}

def should_continue(state: AgentState) -> AgentState:
    messages = state["messages"]
    last_message = messages[-1]
    if not last_message.tool_calls:
        return "end"
    else:
        return "continue"
    
graph = StateGraph(AgentState)

graph.add_node("Agent", chatbot_node)

tool_node = ToolNode(tools=tools)
graph.add_node(tool_node)

graph.set_entry_point("Agent")

graph.add_conditional_edges(
    "Agent",
    should_continue,
    {
        "continue": "tools",
        "end": END
    }
)

graph.add_edge("tools", "Agent")

rag_agent = graph.compile()
