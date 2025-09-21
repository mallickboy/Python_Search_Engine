from typing import List
from functools import partial
import asyncio
from concurrent.futures import ThreadPoolExecutor
from pinecone import Pinecone
from config import (
    PINECONE_ENVIRONMENT, 
    PINECONE_KEY, 
    PINECONE_INDEX, 
    PINECONE_NAMESPACE, 
    PINECONE_RESPONSE_COUNT,
    MAX_CONCURRENT_TASKS
)

# Setting up concurrency limits
SEMAPHORE = asyncio.Semaphore(MAX_CONCURRENT_TASKS)
EXECUTOR = ThreadPoolExecutor(max_workers=MAX_CONCURRENT_TASKS)

def _search_pinecone_db(
    query_vector: List[float],
    api_key: str = PINECONE_KEY,
    environment: str = PINECONE_ENVIRONMENT,
    index_name: str = PINECONE_INDEX,
    namespace: str = PINECONE_NAMESPACE,
    top_k: int = int(PINECONE_RESPONSE_COUNT)
) -> List[dict] :
    try:
        print("Req: ", type(query_vector))
        client=Pinecone(api_key=api_key,environment=environment)
        index=client.Index(index_name)
        result = index.query(
            namespace= namespace,
            vector= query_vector,
            top_k= top_k,
            include_values= False,
            include_metadata= True,
        )
        return result.get('matches', [])
    
    except Exception as e:
        raise RuntimeError(f"Pinecone query failed")

async def search_pinecone(query_vector: List[float]) -> List[dict]:
    async with SEMAPHORE:
        event_loop = asyncio.get_running_loop()
        function = partial(_search_pinecone_db, query_vector= query_vector) 
        return await event_loop.run_in_executor(executor=EXECUTOR, func=function)
