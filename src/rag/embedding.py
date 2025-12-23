from langchain_community.embeddings import OpenAIEmbeddings
from langchain_huggingface.embeddings import HuggingFaceEmbeddings

from enum import Enum
import os
class EmbeddingProvider(Enum):
    HUGGING_FACE = "hugging_face"
    OPENAI = "openai"

def get_embedding_provider(provider : EmbeddingProvider,model_id : str):
    if provider == EmbeddingProvider.HUGGING_FACE:
        return HuggingFaceEmbeddings(model_name = model_id)
    elif provider == EmbeddingProvider.OPENAI:
        return OpenAIEmbeddings(model=model_id, api_key= os.environ.get("OPENAI_API_KEY"))
    return None