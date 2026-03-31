from data import documents
from . import embedding
from data import vectorstore
from .chatbots import chatbot
from typing import List
from langchain_core.documents import Document
from settings.settings import EMBEDDING_MODEL,LLM_MODEL
from .embedding import EmbeddingProvider,get_embedding_provider
from .llm import get_llm,LLM
from .chatbots.chatbot import build_rag_chain

db = vectorstore.VectorStoreManager(
    name = "vietnamese_news",
    type = vectorstore.VectorStore.QDRANT
)
embedding   = get_embedding_provider(EmbeddingProvider.HUGGING_FACE,EMBEDDING_MODEL)
db.build(
    embedder=embedding,
)

llm         = get_llm(LLM.Cloud.DEEPSEEK,LLM_MODEL)
rag_chain   = build_rag_chain(llm,retriever = db.retriver())


def read_doc(datas : List[dict]):
    global db
    db.add(datas)

def chat(message : str , history : List[tuple] = []) :
    print("Chating")
    global rag_chain
    answer = rag_chain.invoke({"input": message})
    print(f"Answer: {answer}")
    return answer["answer"]