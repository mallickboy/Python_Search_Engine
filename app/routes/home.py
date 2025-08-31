from fastapi import APIRouter, Request, HTTPException
from app.services.home import get_home_page

router = APIRouter()

@router.get("/")
async def home(request: Request):
    results = get_home_page(request)
    if "error" in results:
        raise HTTPException(status_code=500, detail=results["error"])
    return results["content"]