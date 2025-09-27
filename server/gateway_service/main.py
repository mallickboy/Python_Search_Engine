from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from search_pipeline import perform_search

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates= Jinja2Templates(directory="templates")

@app.get('/', response_class = HTMLResponse)
async def home(req: Request):
    return templates.TemplateResponse("index.html", {"request": req} )

@app.get('/search')
async def search(q: str):
    return await perform_search(request= q)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port= 4000)