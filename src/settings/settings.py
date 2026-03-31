import os
import dotenv
from dotenv import load_dotenv

load_dotenv(".env")

EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
SENTENCE_TRANFORMER_MODEL = "all-MiniLM-L6-v2"
LLM_MODEL = "deepseek-r1"
PERSIST_DIR = "vectorstore"
CHUNK_SIZE = 500
CHUNK_OVERLAPPED = 200

QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))