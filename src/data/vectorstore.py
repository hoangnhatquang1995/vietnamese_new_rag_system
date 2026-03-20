from __future__ import annotations

from typing import Optional, List, Literal, Any, cast
import os

from langchain_core.vectorstores import VectorStoreRetriever
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_community.docstore import InMemoryDocstore
from langchain_chroma import Chroma
from . import documents

import faiss
import hashlib


VECTORESTORE_PATH = "stored"

def document_id(doc : Document) -> str:
    content = doc.page_content.strip()
    meta = doc.metadata or {}
    meta_part = "|".join(
        str(meta.get(k, ""))
        for k in ("source", "title", "published_time", "news")
    )
    raw = f"{meta_part}\n{content}"
    return hashlib.md5(raw.encode("utf-8")).hexdigest()

class VectorStoreManager:
    embedder: Any = None
    persist_path: str = VECTORESTORE_PATH
    vectorstore: Optional[Chroma] = None

    @staticmethod
    def document_id(doc : Document) -> str:
        content = doc.page_content.strip()
        meta = doc.metadata or {}
        meta_part = "|".join(
            str(meta.get(k, ""))
            for k in ("source", "title", "published_time", "news")
        )
        raw = f"{meta_part}\n{content}"
        return hashlib.md5(raw.encode("utf-8")).hexdigest()

    @staticmethod
    def dict_id(dict: dict) -> str:
        content = str(dict)
        return hashlib.md5(content.encode("utf-8")).hexdigest()
    @staticmethod
    def string_id(string: str) -> str:
        return hashlib.md5(string.encode("utf-8")).hexdigest()
    
    @staticmethod
    def dict_to_document(dic: dict, generate_id: bool = True) -> Document:
        metadata = {
            key: value for key, value in dic.items() if key not in ["text", "id"]
        }
        text = str(dic.get("text", dic))
        doc_id = dic.get("id")
        if generate_id and doc_id is None:
            doc_id = VectorStoreManager.dict_id(dic)
        return Document(
            id=str(doc_id) if doc_id is not None else None,
            page_content=text,
            metadata=metadata,
        )
    
    @staticmethod
    def document_to_dict(doc: Document) -> dict:
        return {
            "id": getattr(doc, "id", None),
            "text": doc.page_content,
            **doc.metadata
        }

    def __init__(self, embedder=None, name="vietnamese_news", persist_path: str = VECTORESTORE_PATH):
        self.embedder = embedder
        self.persist_path = persist_path
        self.name = name

    def build(self, embedder=None, documents: Optional[List[Document]] = None):
        if embedder != None :
            self.embedder = embedder
        print("! BUILD VECTORSTORE !")

        if self.embedder is None:
            raise ValueError("[!Warning] Embedder chưa được cấu hình")
        
        self.vectorstore = Chroma(
            embedding_function=self.embedder,
            persist_directory=self.persist_path,
            collection_name=self.name
        )

        if documents:
            self.add(documents)

        self.save()
        return self.vectorstore
    
    # def read(self, datas: List[dict], embedder=None):
    #     docs = []
    #     for data in datas:
    #         doc = self.dict_to_document(data)
    #         docs.append(doc)
    #     chunks = documents.chunking_document(docs)
    #     if self.vectorstore is None:
    #         self.build(embedder, chunks)
    #     else:
    #         self.add(chunks)
             
        
    def save(self) -> None:
        if self.vectorstore is None:
            raise ValueError("[ERROR] self.vectorstore = NONE")

        os.makedirs(self.persist_path, exist_ok=True)
        persist_fn = getattr(self.vectorstore, "persist", None)
        if callable(persist_fn):
            persist_fn()

    def load(self):
        if self.embedder is None:
            raise ValueError("[!Warning] Embedder chưa được cấu hình")
        os.makedirs(self.persist_path, exist_ok=True)
        self.vectorstore = Chroma(
            embedding_function=self.embedder,
            persist_directory=self.persist_path,
            collection_name="vietnamese_news",
        )

    def add(self, data: Any):
        if self.vectorstore is None:
            raise ValueError("[!Warning] VectorStore chưa được tạo")
        docs: list[Document] = []
        ids : list[str] = []

        if isinstance(data, Document):
            ids  = [self.document_id(data)]
            docs = [data]
        elif isinstance(data, str):
            ids  = [self.string_id(data)]
            docs = [Document(page_content=data, metadata={})]
        elif isinstance(data, dict):
            ids  = [self.dict_id(data)]
            docs = [self.dict_to_document(data)]
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, Document):
                    ids.append(self.document_id(item))
                    docs.append(item)
                elif isinstance(item, str):
                    ids.append(self.string_id(item))
                    docs.append(Document(page_content=item, metadata={}))
                elif isinstance(item, dict):
                    ids.append(self.dict_id(item))
                    docs.append(self.dict_to_document(item))
                else:
                    raise TypeError(f"Không hỗ trợ kiểu phần tử trong list: {type(item)!r}")
        else:
            raise TypeError(f"Không hỗ trợ kiểu dữ liệu: {type(data)!r}")

        if docs:
            self.vectorstore.add_documents(docs, ids=ids)
        self.save()

    def query(self, query : str, top_k : int = 10):
        if self.vectorstore is None:
            raise ValueError("[!Warning] VectorStore chưa được tạo")
        results = self.vectorstore.similarity_search( query, k=top_k )
        return results

    def search(self, search: str, filter: Optional[dict] = None):
        if self.vectorstore is None:
            raise ValueError("[!Warning] VectorStore chưa được tạo")
        filter = filter or {}
        retriever = self.vectorstore.as_retriever(
            search_kwargs={
                "k": 10,
                "filter" : filter
            },
            search_type="similarity",
        )
        docs = retriever.invoke(search)
        return docs
    
    def retriver (self):
        if self.vectorstore is None:
            return None 
        return self.vectorstore.as_retriever(search_kwargs={"k": 10})
    
