import asyncio
import httpx
import ujson
from utils.query_normalizer import QueryRefinementPipeline, save_query_frequency
from agentic_response import rerank_and_answer_with_gemini
from config import (
    EMBEDDING_SERVICE_PORT,
    EMBEDDING_SERVICE_ROUTE,
    SEARCH_SERVICE_PORT,
    SEARCH_SERVICE_ROUTE,
    MAX_CONCURRENT_TASKS
)

SEMAPHORE = asyncio.Semaphore(MAX_CONCURRENT_TASKS)
EMBEDDING_SERVICE_URL = f"http://localhost:{EMBEDDING_SERVICE_PORT}{EMBEDDING_SERVICE_ROUTE}"
SEARCH_SERVICE_URL = f"http://localhost:{SEARCH_SERVICE_PORT}{SEARCH_SERVICE_ROUTE}"
QR_PIPELINE= QueryRefinementPipeline()

CLIENT: httpx.AsyncClient | None = None

def _get_client():
    """Re-use existing else rebuild httpx client"""
    global CLIENT
    if CLIENT is None or (hasattr(CLIENT, 'is_closed') and CLIENT.is_closed):
        CLIENT = httpx.AsyncClient(
            http2=True,
            limits=httpx.Limits(
                max_keepalive_connections=max(MAX_CONCURRENT_TASKS//5, 5),  # 20% idle connections
                max_connections=int(MAX_CONCURRENT_TASKS * 1.2)  # 20% more than max concurrency
            ),
            timeout=10.0
        )
    return CLIENT

async def stop_httpx_client():
    global CLIENT
    if CLIENT is not None:
        await CLIENT.aclose()
        CLIENT = None

async def pipeline(query):
    global CLIENT

    try:
        client = _get_client()
        processed_query = QR_PIPELINE.process(query=query)['normalized']
        save_query_frequency(processed_query)
        r = await client.get(f"{EMBEDDING_SERVICE_URL}?sentence={processed_query}")
        r.raise_for_status()
        vector_response = ujson.loads(r.text)
        vector = vector_response.get("vector", [])

        r2 = await client.post(SEARCH_SERVICE_URL, json={"query_vector": vector})
        r2.raise_for_status()
        search_response = ujson.loads(r2.text)
        return search_response
    except Exception as e:
        print(f"Pipeline error: {e}")
        if CLIENT is not None:
            await CLIENT.aclose()
            CLIENT = None  # client is recreated on next use
        return None

async def perform_search(request):
    async with SEMAPHORE:
        return await pipeline(query=request)
