from typing import List, Dict, Any
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

PC_CLIENT = Pinecone(api_key=PINECONE_KEY, environment=PINECONE_ENVIRONMENT)
INDEX = PC_CLIENT.Index(PINECONE_INDEX)


def _search_pinecone_db(
    query_vector: List[float],
    api_key: str = PINECONE_KEY,
    environment: str = PINECONE_ENVIRONMENT,
    index_name: str = PINECONE_INDEX,
    namespace: str = PINECONE_NAMESPACE,
    top_k: int = int(PINECONE_RESPONSE_COUNT)
) -> List[Dict[str, Any]] :
    """Search in pinecone and return raw matches"""
    try:
        # client=Pinecone(api_key=api_key,environment=environment)
        # index=client.Index(index_name)
        result = INDEX.query(
            namespace= namespace,
            vector= query_vector,
            top_k= top_k,
            include_values= False,
            include_metadata= True,
        )
        return result.get('matches', [])
    
    except Exception as e:
        raise RuntimeError(f"Pinecone query failed")

def _process_matches(matches: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """ Takes raw pinecone matches , keep unique title pages and refactor page in dict and return list of such ditcs"""
    seen_titles, cleaned_results = set(), []

    for page in matches:
        metadata = page.get("metadata", {})
        title = metadata.get("title")

        if not title or title in seen_titles:
            continue
        seen_titles.add(title)

        link = metadata.get("link")
        desc_raw = metadata.get("desc", "")
        desc = " ".join(desc_raw.split("|@|") if desc_raw else [])

        h1 = metadata.get("h1", "")
        h2 = metadata.get("h2", "")
        
        cleaned_results.append({
            "title": title,
            "link": link,
            "desc": desc,
            "h1": h1.split("|@|") if h1 else [],
            "h2": h2.split("|@|") if h2 else [],
        })

    return cleaned_results

async def search_pinecone(query_vector: List[float]) -> List[dict]:
    """Leverages pinecone search and refactor leveraging dedicated function """
    async with SEMAPHORE:
        event_loop = asyncio.get_running_loop()
        function = partial(_search_pinecone_db, query_vector= query_vector) 
        matches = await event_loop.run_in_executor(executor=EXECUTOR, func=function)
        return _process_matches(matches)
