import os
import dotenv
from dotenv import load_dotenv

load_dotenv(".env")

HUGGINGFACE_MODEL_NAME = "BAAI/bge-small-en-v1.5"
SENTENCE_TRANFORMER_MODEL = "all-MiniLM-L6-v2"
PERSIST_DIR = "vectorstore"