import asyncio
from functools import partial
from typing import List
from concurrent.futures import ThreadPoolExecutor
from sentence_transformers import SentenceTransformer
from config import (
    SENTENCE_TRANSFORMER_MODEL,
    MAX_CONCURRENT_TASKS
)

# Setting concurrency limits
EXECUTOR = ThreadPoolExecutor(max_workers=MAX_CONCURRENT_TASKS)
SEMAPHORE = asyncio.Semaphore(value=MAX_CONCURRENT_TASKS)

# Loading the sentence transformer model for sentence embedding
MODEL = SentenceTransformer(SENTENCE_TRANSFORMER_MODEL)

def vectorize_query(sentence: str) -> List[float]:
    """Takes sentence and convert them to vectors"""
    return MODEL.encode(sentence).tolist()

async def async_vectorize_query(sentence: str) -> List[float]:
    """Async wrapper to offload sync embedding to thread"""
    async with SEMAPHORE:
        event_loop = asyncio.get_running_loop()
        function = partial(vectorize_query, sentence) 
        return await event_loop.run_in_executor(executor=EXECUTOR, func=function)