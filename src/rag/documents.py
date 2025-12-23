from typing import Annotated,Optional,List
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

def to_document(dict : dict):
    return Document(
        page_content=dict["content"],
        metadata={
            "url": dict["url"],
            "title": dict["title"],
            "published_time": dict["published_time"],
            "images": dict["images"],
            "source": "vnexpress",
        }
    )

def to_list_documents(dicts : List[dict]):
    docs = []
    for dict in dicts:
        docs.append(to_document(dict))
    return docs

def chunking_document(docs : List[Document]):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500,
                                      chunk_overlap=200,)
    esops_documents = text_splitter.transform_documents(docs)
    return esops_documents