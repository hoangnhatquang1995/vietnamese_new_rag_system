from llama_index.core import VectorStoreIndex,StorageContext,load_index_from_storage
from llama_index.core import Document
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.response_synthesizers import get_response_synthesizer
from llama_index.core.node_parser import TokenTextSplitter
from typing import Optional
from src.data.rss import request_rss_data

def build_index(documents,save_dir:Optional[str] = None) -> VectorStoreIndex:
    splitter = TokenTextSplitter(
    chunk_size=512,
        chunk_overlap=10,
        separator=" ",
    )
    nodes = splitter.get_nodes_from_documents(
        documents= documents
    )
    index = VectorStoreIndex(nodes)
    if save_dir and len(save_dir) > 0 :
        index.storage_context.persist(
            persist_dir = save_dir
    )
    return index

def load_index(persis_dir : str) -> VectorStoreIndex :
    storage_context = StorageContext.from_defaults(persist_dir=persis_dir)
    index = load_index_from_storage(storage_context)
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