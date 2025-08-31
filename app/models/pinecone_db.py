import time
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
from app.config import PINECONE_KEY, PINECONE_ENVIRONMENT, PINECONE_INDEX, SENTENCE_TRANSFORMER

# Initialize model once per worker
MODEL = SentenceTransformer(SENTENCE_TRANSFORMER)


def init_pinecone_index(retries=3, delay=2):
    for i in range(retries):
        try:
            pc = Pinecone(api_key=PINECONE_KEY, environment=PINECONE_ENVIRONMENT)
            index = pc.Index(PINECONE_INDEX)
            return pc, index
        except Exception as e:
            print(f"Pinecone init failed: {e}, retrying in {delay}s")
            time.sleep(delay)
            delay *= 2  # exponential backoff
    raise RuntimeError("Failed to initialize Pinecone after retries")

# Initialize once per worker
PC, INDEX = init_pinecone_index()

def query_pinecone(vector, top_k=50, namespace="ns2"):
    global INDEX, PC
    try:
        return INDEX.query(
            vector=vector,
            top_k=top_k,
            namespace=namespace,
            include_values=False,
            include_metadata=True
        )['matches']
    except Exception as e:
        print(f"Pinecone query failed: {e}, trying to reconnect...")
        PC, INDEX = init_pinecone_index()
        try:
            return INDEX.query(
                vector=vector,
                top_k=top_k,
                namespace=namespace,
                include_values=False,
                include_metadata=True
            )['matches']
        except Exception as e2:
            print(f"Pinecone retry failed: {e2}")
            return []
