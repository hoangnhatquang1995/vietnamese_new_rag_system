import os
import dotenv
from dotenv import load_dotenv

from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings
from llama_index.llms.gemini import Gemini

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
MODEL_NAME = os.environ.get("MODEL_NAME")
HUGGINGFACE_MODEL_NAME = os.environ.get("HUGGINGFACE_MODEL_NAME")

gemini = Gemini(api_key= GEMINI_API_KEY ,model = MODEL_NAME)
embedded = HuggingFaceEmbedding(model_name= HUGGINGFACE_MODEL_NAME)

Settings.llm = gemini
Settings.embed_model = embedded
