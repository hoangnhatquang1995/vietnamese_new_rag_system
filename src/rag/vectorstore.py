from typing import Optional,List
import os

from langchain_core.vectorstores import VectorStoreRetriever
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_community.docstore import InMemoryDocstore
import faiss
import hashlib


VECTORESTORE_PATH = "stored"
VectorStoreType = FAISS

def document_id(doc : Document) -> str:
    content = doc.page_content.strip()
    return hashlib.md5(content.encode("utf-8")).hexdigest()

class VectorStoreManager:
    embedder :any = None
    persist_path: str = VECTORESTORE_PATH
    vectorstore : Optional[VectorStoreType] = None

    def __init__(self, embedder = None,persist_path = VECTORESTORE_PATH):
        self.embedder = embedder
        self.persist_path = persist_path
        
    def build(self,embedder = None, documents : List[Document] = []):
        if embedder != None :
            self.embedder = embedder
        print("! BUILD VECTORSTORE !")
        dim = len(self.embedder.embed_query(" "))
        index = faiss.IndexFlatL2(dim)
        self.vectorstore = FAISS(
            embedding_function=self.embedder,
            index=index,
            docstore=InMemoryDocstore(),
            index_to_docstore_id={}
        )
        if len(documents) > 0:
            self.vectorstore.add_documents(documents)
        if not os.path.exists(self.persist_path):
            self.save()
        return self.vectorstore

    def save(self):
        print("!SAVING VECTORSTORE TO LOCAL!")
        if self.vectorstore is None:
            raise ValueError("[!Warning] VectorStore chưa được tạo")
        self.vectorstore.save_local(self.persist_path)

    def load(self,embedder = None,build_if_not_existed = True):
        if embedder != None :
            self.embedder = embedder
        if not os.path.exists(self.persist_path):
            if build_if_not_existed:
                return self.build()
            return None
        self.vectorstore = FAISS.load_local(
            self.persist_path,
            embeddings=self.embedder,
            allow_dangerous_deserialization=True
        )

        return self.vectorstore

    def add(self,documents : List[Document], update_if_exist = False):
        if self.vectorstore is None:
            raise ValueError("[!Warning] VectorStore chưa được tạo")
        new_docs = []
        new_ids = []

        for doc in documents:
            doc_id = document_id(doc)

            exists = doc_id in self.vectorstore.docstore._dict
            if exists and not update_if_exist:
                continue

            if exists and update_if_exist:
                self.vectorstore.delete([doc_id])

            new_docs.append(doc)
            new_ids.append(doc_id)

        if new_docs:
            self.vectorstore.add_documents(new_docs, ids=new_ids)
            if os.path.exists(self.persist_path):
                self.save()

    def search(self, search : str, filter : dict = {}):
        if self.vectorstore is None:
            raise ValueError("[!Warning] VectorStore chưa được tạo")
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
    
    


# def build_from_document(documents , embedder_model) -> FAISS:
#     # vectorstore = FAISS.from_documents( 
#     #     documents= documents,
#     #     embedding= embedder_model
#     # )
#     # return vectorstore

#     dim = len(embedder_model.embed_query(" "))
#     index = faiss.IndexFlatL2(dim)
#     vector_store = FAISS(
#         embedding_function=embedder_model,
#         index=index,
#         docstore=InMemoryDocstore(),
#         index_to_docstore_id={}
#     )
#     vector_store.add_documents(documents)
#     return vector_store

# def save_vectorstore(vectorstore : FAISS):
#     vectorstore.save_local(VECTORESTORE_PATH)

# def load_vectorstore(embedder_model):
#     vectorstore = FAISS.load_local(
#         VECTORESTORE_PATH,
#         embeddings= embedder_model,
#         allow_dangerous_deserialization= True
#     )
#     return vectorstore

# def add_documents(
#     vectorstore: FAISS,
#     documents: List[Document],
#     update_if_exists: bool = False
# ):

#     docs = []
#     ids = []

#     for doc in documents:
#         doc_id = document_id(doc)

#         if doc_id in vectorstore.docstore._dict:
#             if update_if_exists:
#                 vectorstore.delete([doc_id])
#             else:
#                 continue

#         docs.append(doc)
#         ids.append(doc_id)

#     if docs:
#         vectorstore.add_documents(docs, ids=ids)


# def search_document_from_vectorstore(search : str, vectorstore : FAISS ,filter : dict = {}):
#     retriever = vectorstore.as_retriever(
#         search_kwargs={
#             "k": 10,
#             "filter" : filter
#         },
#         search_type="similarity",
#     )
#     docs = retriever.invoke(search)
#     return docs

