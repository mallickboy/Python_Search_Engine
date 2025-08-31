import os
from dotenv import load_dotenv
load_dotenv()

SENTENCE_TRANSFORMER = os.getenv("SENTENCE_TRANSFORMER", "msmarco-distilbert-base-v3")
PINECONE_KEY = os.getenv("PINECONE_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
PINECONE_INDEX = os.getenv("PINECONE_INDEX", "search")
PINECONE_NAMESPACE = os.getenv("PINECONE_NAMESERVER", "ns2")
PINECONE_SEARCH_RESULTS = int(os.getenv("PINECONE_SEARCH_RESULTS", 50))
