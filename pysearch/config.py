import os
from dotenv import load_dotenv
from pathlib import Path
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer

MODEL=SentenceTransformer("msmarco-distilbert-base-v3")

ENV_PATH = Path(os.environ.get("SNAP_USER_COMMON", "./common")) / ".env"
load_dotenv(dotenv_path=ENV_PATH)

PINECONE_KEY = os.getenv("PINECONE_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")

try:
    GET_RESULT_COUNT = int(os.getenv("GET_RESULT_COUNT"))
except:
    GET_RESULT_COUNT = 50

if not PINECONE_KEY or not PINECONE_ENVIRONMENT:
    raise RuntimeError("Missing Pinecone credentials")

SEARCH_CLIENT = Pinecone(api_key=PINECONE_KEY, environment=PINECONE_ENVIRONMENT)
