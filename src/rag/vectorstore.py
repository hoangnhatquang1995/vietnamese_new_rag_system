from __future__ import annotations

from typing import Optional, List, Literal, Any, cast
import os

from langchain_core.vectorstores import VectorStoreRetriever
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_community.docstore import InMemoryDocstore

from . import documents

import faiss
import hashlib


VECTORESTORE_PATH = "stored"
VectorBackend = Literal["faiss", "chroma"]
VectorStoreType = Any

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
    vectorstore: Optional[VectorStoreType] = None
    backend: VectorBackend = "faiss"

    def __init__(self, embedder=None, persist_path: str = VECTORESTORE_PATH, backend: VectorBackend = "faiss"):
        self.embedder = embedder
        self.persist_path = persist_path
        self.backend = backend
        
    def build(self, embedder=None, documents: Optional[List[Document]] = None):
        if embedder != None :
            self.embedder = embedder
        print("! BUILD VECTORSTORE !")

        if self.embedder is None:
            raise ValueError("[!Warning] Embedder chưa được cấu hình")

        if self.backend == "chroma":
            try:
                from langchain_community.vectorstores import Chroma
            except Exception as e:
                raise ImportError(
                    "Chroma backend requires `chromadb`. Install it or use backend='faiss'."
                ) from e
            self.vectorstore = Chroma(
                embedding_function=self.embedder,
                persist_directory=self.persist_path,
                collection_name="vietnamese_news",
            )
        else:
            dim = len(self.embedder.embed_query(" "))
            index = faiss.IndexFlatL2(dim)
            self.vectorstore = FAISS(
                embedding_function=self.embedder,
                index=index,
                docstore=InMemoryDocstore(),
                index_to_docstore_id={},
            )

        if documents:
            self.add(documents, update_if_exist=False)

        self.save()
        return self.vectorstore
    
    def read(self, datas: List[dict], embedder=None):
        docs = documents.to_list_documents(datas)
        chunks = documents.chunking_document(docs)
        if self.vectorstore is None:
            self.build(embedder, chunks)
        else:
            self.add(chunks)
             
        
    def save(self):
        print("!SAVING VECTORSTORE TO LOCAL!")
        if self.vectorstore is None:
            raise ValueError("[!Warning] VectorStore chưa được tạo")

        os.makedirs(self.persist_path, exist_ok=True)
        # FAISS + Chroma both support persistence, but method names differ.
        if hasattr(self.vectorstore, "save_local"):
            self.vectorstore.save_local(self.persist_path)
        elif hasattr(self.vectorstore, "persist"):
            self.vectorstore.persist()

    def load(self, embedder=None, build_if_not_existed=True):
        if embedder != None :
            self.embedder = embedder
        if not os.path.exists(self.persist_path):
            if build_if_not_existed:
                print("Build instead of Load Local")
                return self.build()
            return None
        print("Load from Local")

        if self.backend == "chroma":
            try:
                from langchain_community.vectorstores import Chroma
            except Exception as e:
                raise ImportError(
                    "Chroma backend requires `chromadb`. Install it or use backend='faiss'."
                ) from e
            self.vectorstore = Chroma(
                embedding_function=self.embedder,
                persist_directory=self.persist_path,
                collection_name="vietnamese_news",
            )
        else:
            self.vectorstore = FAISS.load_local(
                self.persist_path,
                embeddings=self.embedder,
                allow_dangerous_deserialization=True,
            )

        return self.vectorstore

    def add(self, documents: List[Document], update_if_exist=False):
        if self.vectorstore is None:
            raise ValueError("[!Warning] VectorStore chưa được tạo")
        new_docs = []
        new_ids = []

        for doc in documents:
            doc_id = document_id(doc)

            # Works for FAISS; for other stores we best-effort add.
            exists = False
            if hasattr(self.vectorstore, "docstore") and hasattr(self.vectorstore.docstore, "_dict"):
                store_dict = cast(Any, self.vectorstore.docstore)._dict
                exists = doc_id in store_dict
            if exists and not update_if_exist:
                continue

            if exists and update_if_exist:
                self.vectorstore.delete([doc_id])

            new_docs.append(doc)
            new_ids.append(doc_id)

        if new_docs:
            if self.backend == "faiss":
                self.vectorstore.add_documents(new_docs, ids=new_ids)
            else:
                self.vectorstore.add_documents(new_docs)
            self.save()

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
    
