import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path("../.env")

load_dotenv(dotenv_path= env_path)

PINECONE_KEY = os.getenv("PINECONE_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
PINECONE_INDEX = os.getenv("PINECONE_INDEX")
PINECONE_NAMESPACE = os.getenv("PINECONE_NAMESPACE")
PINECONE_RESPONSE_COUNT = os.getenv("PINECONE_RESPONSE_COUNT")

MAX_CONCURRENT_TASKS = 30

