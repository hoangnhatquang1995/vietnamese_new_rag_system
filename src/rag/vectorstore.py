from typing import Optional

from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_classic.storage import LocalFileStore
from langchain_classic.embeddings import CacheBackedEmbeddings

from settings.settings import HUGGINGFACE_MODEL_NAME

def build_from_document(documents , embedder_model ) :
    vectorstore = Chroma.from_documents( 
        documents= documents,
        embedding= embedder_model
    )
    return vectorstore.as_retriever()



