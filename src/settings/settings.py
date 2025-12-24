import os
import dotenv
from dotenv import load_dotenv

load_dotenv(".env")

HUGGINGFACE_MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
SENTENCE_TRANFORMER_MODEL = "all-MiniLM-L6-v2"
OPENAI_MODEL = "gemini-2.5-flash"
PERSIST_DIR = "vectorstore"
CHUNK_SIZE = 500
CHUNK_OVERLAPPED = 200