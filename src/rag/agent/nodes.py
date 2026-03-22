from langchain.messages import AnyMessage,HumanMessage,AIMessage,SystemMessage
from langgraph.prebuilt import ToolNode
from rag.agent.state import AgentState
from rag.agent.tools import tools
from rag.chatbots.chatbot import build_rag_chain

def planner_node(state : AgentState) -> dict:
    return {}

def chatbot_node(state : AgentState) -> dict:
    return {}

tool_node = ToolNode(tools = [tool for tool in tools.values()])