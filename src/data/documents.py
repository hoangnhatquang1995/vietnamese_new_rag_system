from typing import Annotated,Optional,List
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from settings.settings import CHUNK_SIZE,CHUNK_OVERLAPPED

def chunking_document(docs : List[Document]):
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAPPED
    )
    # esops_documents = text_splitter.transform_documents(docs)
    esops_documents = text_splitter.split_documents(documents= docs)
    return esops_documents

