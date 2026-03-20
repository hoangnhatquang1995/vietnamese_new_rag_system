from dotenv import load_dotenv
import os

from langchain_classic.chat_models.ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai.chat_models import ChatGoogleGenerativeAIError
from langchain_openai.chat_models import ChatOpenAI
from langchain.chat_models import init_chat_model,BaseChatModel

from enum import Enum 

load_dotenv()

class LLM :
    class Cloud(Enum) :
        GOOGLE_CHAT = "google_chat"
        OPEN_AI = "openai"
        DEEPSEEK = "deepseek"
    class Local(Enum):
        OLLAMA = "ollama"   # For Local Model (WARNING : không có with_structured_output thực sự)
        LM_STUDIO = "lm_studio"

def get_llm(llm : LLM.Cloud | LLM.Local , model : str,temperature: float = 0.3) ->  BaseChatModel | None:
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
    elif llm == LLM.Cloud.DEEPSEEK:
        return init_chat_model(
            model = "deepseek-chat",
            model_provider= "deepseek",
            api_key = os.getenv("DEEPSEEK_API_KEY"),
            temperature= temperature,
            max_tokens= 2048,
        )
    elif llm == LLM.Local.OLLAMA :
        print("GET OLLAMA")
        return ChatOllama(
            model= model,
            temperature= temperature
        )
    elif llm == LLM.Local.LM_STUDIO:
        return init_chat_model(
            model = model,
            model_provider= "lm_studio",
            api_key = os.getenv("LM_STUDIO_API_KEY"),
            temperature= temperature,
            max_tokens= 2048,
        )
    return None


