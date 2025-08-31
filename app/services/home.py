from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

templates = Jinja2Templates(directory="app/templates")

def get_home_page(request: Request):
    """
    Returns the homepage template response.
    """
    try:
        return {"content":templates.TemplateResponse("index.html", {"request": request})}
    except Exception as e:
        return {"error": str(e)}
