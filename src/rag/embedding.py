from langchain_community.embeddings import OpenAIEmbeddings
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_ollama import OllamaEmbeddings

from enum import Enum
import os
class EmbeddingProvider(Enum):
    HUGGING_FACE = "hugging_face"
    OPENAI = "openai"
    OLLAMA = "ollama" #For Running Local

def get_embedding_provider(provider : EmbeddingProvider,model_id : str):
    if provider == EmbeddingProvider.HUGGING_FACE:
        return HuggingFaceEmbeddings(model_name = model_id)
    elif provider == EmbeddingProvider.OPENAI:
        return OpenAIEmbeddings(model=model_id, api_key= os.environ.get("OPENAI_API_KEY"))
    elif provider == EmbeddingProvider.OLLAMA:
        return OllamaEmbeddings(model=model_id)
    return None

def get_embedding_dimension(provider : EmbeddingProvider, model_id : str) -> int:
    embedder = get_embedding_provider(provider, model_id)
    if embedder is not None:
        return len(embedder.embed_query("test"))
    else:
        raise ValueError(f"Unsupported embedding provider: {provider}")