import random
import asyncio
from config import (
    GATEWAY_SERVICE_PORT,
    GATEWAY_SERVICE_ROUTE,
    EMBEDDING_SERVICE_PORT,
    EMBEDDING_SERVICE_ROUTE,
    SEARCH_SERVICE_PORT,
    SEARCH_SERVICE_ROUTE,
    MAX_CONCURRENT_TASKS
)

SEMAPHORE = asyncio.Semaphore(MAX_CONCURRENT_TASKS)

async def random_response(count: int = 3):
    return random.choices(
        [
        {"title": "Array in java", "link": "https://www.javatpoint.com/array-in-java", "desc": "Array in java"},
        {"title": "What is an array", "link": "https://www.geeksforgeeks.org/what-is-array", "desc": "What is an array"},
        {"title": "Java tutorial", "link": "https://www.w3schools.com/java", "desc": "Java tutorial"},
        {"title": "Python tutorial", "link": "https://www.w3schools.com/python", "desc": "Python tutorial"},
        {"title": "Golang Concurrency", "link": "https://www.w3schools.com/golang", "desc": "Golang Concurrency"}
    ],
    k= count
    )

async def perform_search(request):
    print((
    GATEWAY_SERVICE_PORT,
    GATEWAY_SERVICE_ROUTE,
    EMBEDDING_SERVICE_PORT,
    EMBEDDING_SERVICE_ROUTE,
    SEARCH_SERVICE_PORT,
    SEARCH_SERVICE_ROUTE
))  
    async with SEMAPHORE:
        return await random_response()