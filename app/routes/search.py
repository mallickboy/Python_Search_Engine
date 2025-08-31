from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import JSONResponse
from app.services.search import perform_search

router = APIRouter()

@router.get("/search")
async def search(q: str = Query(..., min_length=1)):
    results = perform_search(q)
    if "error" in results:
        raise HTTPException(status_code=500, detail=results["error"])
    return JSONResponse(content=results)
