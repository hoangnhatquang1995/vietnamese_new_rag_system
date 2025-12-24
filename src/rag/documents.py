from typing import Annotated,Optional,List
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from settings.settings import CHUNK_SIZE,CHUNK_OVERLAPPED

def to_document(dict : dict):
    return Document(
        page_content=dict["content"],
        metadata={
            "source": dict["source"],
            "title": dict["title"],
            "published_time": dict["published_time"],
            "news": dict["news"],
        }
    )

def to_list_documents(dicts : List[dict]):
    docs = []
    for dict in dicts:
        docs.append(to_document(dict))
    return docs

def chunking_document(docs : List[Document]):
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAPPED
    )
    # esops_documents = text_splitter.transform_documents(docs)
    esops_documents = text_splitter.split_documents(documents= docs)
    return esops_documents

def format_docs(docs : List[Document]):
    return "\n".join(f"<doc{i+1}>:\nTitle:{doc.metadata['title']}\nSource:{doc.metadata['source']}\nContent:{doc.page_content}\n</doc{i+1}>\n" for i, doc in enumerate(docs))
