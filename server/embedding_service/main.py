from pydantic import BaseModel
from typing import List
from fastapi import FastAPI, Query
from vectorizer import async_vectorize_query
from config import (
    EMBEDDING_SERVICE_PORT,
    EMBEDDING_SERVICE_ROUTE
)

app = FastAPI()

class VectorResponse(BaseModel):
    query: str
    vector: List[float]

@app.get(EMBEDDING_SERVICE_ROUTE, response_model= VectorResponse) # /vectorizer?sentence
async def embedding(sentence: str) -> VectorResponse:
    """
    Accepts a sentence via query param and returns its embedding vector.
    """
    vector = await async_vectorize_query(sentence = sentence)

    return VectorResponse(query=sentence, vector=vector)

if __name__== "__main__":
    import uvicorn
    uvicorn.run(app, host= "0.0.0.0", port= EMBEDDING_SERVICE_PORT)