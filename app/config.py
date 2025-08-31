import os
from dotenv import load_dotenv

# loads .env locally; ignored in Docker if env vars already set
load_dotenv() 

SENTENCE_TRANSFORMER = os.getenv("SENTENCE_TRANSFORMER", "msmarco-distilbert-base-v3")
MODEL_CACHE = os.getenv("TRANSFORMERS_CACHE", "./model_cache")
PINECONE_KEY = os.getenv("PINECONE_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
PINECONE_INDEX = os.getenv("PINECONE_INDEX")
PINECONE_NAMESPACE = os.getenv("PINECONE_NAMESPACE")
PINECONE_SEARCH_RESULTS = int(os.getenv("PINECONE_SEARCH_RESULTS", 50))

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))
WORKERS = int(os.getenv("WORKERS", 2))
TIMEOUT = int(os.getenv("TIMEOUT", 120))
