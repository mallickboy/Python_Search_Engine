from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.routes.home import router as home_router
from app.routes.search import router as search_router

def create_app() -> FastAPI:
    app = FastAPI(title="PySearch API")

    # Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Mount static files
    app.mount("/static", StaticFiles(directory="app/static"), name="static")

    # Include routers
    app.include_router(home_router)
    app.include_router(search_router)

    return app
