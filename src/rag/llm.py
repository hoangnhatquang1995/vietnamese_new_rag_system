from langchain_classic.chat_models.ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai.chat_models import ChatGoogleGenerativeAIError
from langchain_openai.chat_models import ChatOpenAI


from enum import Enum 

class LLM :
    class Cloud(Enum) :
        GOOGLE_CHAT = "google_chat"
        OPEN_AI = "openai"
    class Local(Enum):
        OLLAMA = "ollama"   # For Local Model (WARNING : không có with_structured_output thực sự)


def get_llm(llm : LLM.Cloud | LLM.Local , model : str,temperature: float = 0.3) -> ChatGoogleGenerativeAI | ChatOpenAI | ChatOllama :
    if llm == LLM.Cloud.GOOGLE_CHAT:
        return ChatGoogleGenerativeAI(
            model=model,
            temperature=0.3
        )
    elif llm == LLM.Cloud.OPEN_AI:
        return ChatOpenAI(
            model = model,
            temperature= temperature
        )
    elif llm == LLM.Local.OLLAMA :
        return ChatOllama(
            model= model,
            temperature= temperature
        )
    return None

