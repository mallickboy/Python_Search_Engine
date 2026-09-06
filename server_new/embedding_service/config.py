"""Config script to load environment variables."""

import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path("../.env")

load_dotenv(dotenv_path=env_path)

# General config
EMBEDDING_SERVICE_PORT = int(os.getenv("EMBEDDING_SERVICE_PORT") or 4001)
EMBEDDING_SERVICE_CONCURRENCY = int(
    os.getenv("EMBEDDING_SERVICE_CONCURRENCY") or 2,
)
EMBEDDING_SERVICE_ROUTE = os.getenv("EMBEDDING_SERVICE_ROUTE") or "/vectorizer"

MAX_CONCURRENT_TASKS = EMBEDDING_SERVICE_CONCURRENCY

# Service specific config
SENTENCE_TRANSFORMER_MODEL = os.getenv("SENTENCE_TRANSFORMER_MODEL")


# SENTENCE_TRANSFORMER_MODEL = "msmarco-distilbert-base-v3" # v2 good & slow
# SENTENCE_TRANSFORMER_MODEL_NEW = "msmarco-MiniLM-L6-v3" # good and fast
# SENTENCE_TRANSFORMER_MODEL = "multi-qa-MiniLM-L6-cos-v1"
