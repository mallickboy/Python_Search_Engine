"""Main script to run microservice for vector embedding."""

from typing import List
from pydantic import BaseModel
from fastapi import FastAPI
from vectorizer import async_vectorize_query
from config import EMBEDDING_SERVICE_PORT, EMBEDDING_SERVICE_ROUTE

app = FastAPI()


class VectorResponse(BaseModel):
    """Response model containing the query and its embedding vector."""

    query: str
    vector: List[float]


@app.get(EMBEDDING_SERVICE_ROUTE, response_model=VectorResponse)
async def embedding(sentence: str) -> VectorResponse:  # /vectorizer?sentence
    """Accept a sentence via query param and returns its embedding vector."""
    vector = await async_vectorize_query(sentence=sentence)

    return VectorResponse(query=sentence, vector=vector)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=EMBEDDING_SERVICE_PORT)
