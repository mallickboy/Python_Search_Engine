import asyncio
import httpx
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

CLIENT: httpx.AsyncClient | None = None

def _get_client():
    """Re-use existing else rebuild httpx client"""
    global CLIENT
    if CLIENT is None or (hasattr(CLIENT, 'is_closed') and CLIENT.is_closed):
        CLIENT = httpx.AsyncClient()
    return CLIENT

async def pipeline(query):
    global CLIENT

    try:
        client = _get_client()
        r = await client.get(f"{EMBEDDING_SERVICE_URL}?sentence={query}")
        r.raise_for_status()
        vector_response = r.json()
        vector = vector_response.get("vector", [])

        r2 = await client.post(SEARCH_SERVICE_URL, json={"query_vector": vector})
        r2.raise_for_status()
        search_response = r2.json()
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
