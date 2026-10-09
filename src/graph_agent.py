from dotenv import load_dotenv
import os
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, ToolMessage
from langgraph.graph.message import add_messages
import config
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
from langchain_google_genai import ChatGoogleGenerativeAI

from tools import all_tools

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    system_prompt: str

# FIX 1: Unpack tools correctly (was [[tool1, tool2, ...]])
tools = all_tools

llm = ChatGoogleGenerativeAI(model=config.MODEL, api_key=config.API_KEY).bind_tools(tools)

def chatbot_node(state: AgentState) -> AgentState:
    messages = [SystemMessage(content=state["system_prompt"])] + state["messages"]
    return {"messages": [llm.invoke(messages)]}

# FIX 2: Return string, not AgentState
def should_continue(state: AgentState) -> str:
    messages = state["messages"]
    last_message = messages[-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "continue"
    else:
        return "end"

graph = StateGraph(AgentState)

graph.add_node("Agent", chatbot_node)

# FIX 3: Name the tool_node explicitly as "tools"
tool_node = ToolNode(tools=tools)
graph.add_node("tools", tool_node)

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

# FIX 4: Add MemorySaver for conversation persistence
memory = MemorySaver()
rag_agent = graph.compile(checkpointer=memory)