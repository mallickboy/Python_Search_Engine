from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
from cosine_search import search_pinecone

app = FastAPI()

@app.post("/search")
async def search_vector(query_vector: str) -> dict:
    res= await search_pinecone(query_vector= query_vector)
    return {"pinecone_credential": res}

if __name__== "__main__":
    import uvicorn
    uvicorn.run(app, host= "0.0.0.0", port= 4001)