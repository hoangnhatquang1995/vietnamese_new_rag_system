from . import documents
from . import embedding
from . import vectorstore
from . import qa
from typing import List
from langchain_core.documents import Document
from settings.settings import EMBEDDING_MODEL,LLM_MODEL
from .embedding import EmbeddingProvider,get_embedding_provider
from .llm import get_llm,LLM
from .qa import build_rag_chain

db = vectorstore.VectorStoreManager()
embedding   = get_embedding_provider(EmbeddingProvider.HUGGING_FACE,EMBEDDING_MODEL)
db.load(embedding)
llm         = get_llm(LLM.Local.OLLAMA,LLM_MODEL)
rag_chain   = build_rag_chain(llm,retriever = db.retriver())


def read_doc(datas : List[dict]):
    global db
    db.read(datas, embedding)

def chat(message : str) :
    print("Chating")
    global rag_chain
    answer= rag_chain.invoke({"input": message})
    return answer["answer"]