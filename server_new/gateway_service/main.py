from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
from pydantic import BaseModel
from typing import List
from search_pipeline import perform_search, stop_httpx_client
from agentic_response import rerank_and_answer_with_gemini
from config import (
    GATEWAY_SERVICE_PORT,
    GATEWAY_SERVICE_ROUTE
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic 
    yield
    # Shutdown logic
    await stop_httpx_client()

class QnaRequest(BaseModel):
    query: str
    responses: List[dict]

app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates= Jinja2Templates(directory="templates")

@app.get('/', response_class = HTMLResponse)
async def home(req: Request):
    return templates.TemplateResponse("index.html", {"request": req} )

@app.post('/qna')
async def llm_response(data: QnaRequest):
    try:
        query = data.query
        responses = data.responses
        res = await rerank_and_answer_with_gemini(query, responses)
        return {
            "query": query,
            "answer": res
        }
    except Exception as e:
        print(f"Server Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get(GATEWAY_SERVICE_ROUTE)
async def search(q: str):
    return await perform_search(request= q)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=GATEWAY_SERVICE_PORT)