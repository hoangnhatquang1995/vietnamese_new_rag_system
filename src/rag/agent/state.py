from langgraph.graph.message import add_messages 

from typing import TypedDict,Optional,List,Annotated,Dict
from langchain.messages import AnyMessage
from pydantic import BaseModel, Field

class AgentState(TypedDict):
    messages : Annotated[List[AnyMessage], add_messages]
    