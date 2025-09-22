from typing import List, Dict, Any
from fastapi import FastAPI
from pydantic import BaseModel
from cosine_search import search_pinecone

app = FastAPI()

class SearchRequest(BaseModel):
    query_vector: List[float]

@app.post("/search", response_model= List[Dict[str, Any]])
async def search_vector(request: SearchRequest) -> List[Dict[str, Any]]:
    """
    Accepts a vector and returns list of dictionary each ahving page metadata.
    """
    res= await search_pinecone(query_vector= request.query_vector)
    return res

if __name__== "__main__":
    import uvicorn
    uvicorn.run(app, host= "0.0.0.0", port= 4001)