from llama_index.core import VectorStoreIndex
from llama_index.core import Document
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.response_synthesizers import get_response_synthesizer

from src.data.rss import request_rss_data

def build_indexing(documents : Document) -> VectorStoreIndex:
    index = VectorStoreIndex.from_documents(documents=documents)
    return index

def build_engine(index, prompt) -> RetrieverQueryEngine:
    retriever = VectorIndexRetriever(
        index = index,
        similarity_top_k= 3
    )
    response = get_response_synthesizer(
        text_qa_template= prompt
    )
    engine = RetrieverQueryEngine(
        retriever=retriever,
        response_synthesizer=response
    )
    return engine