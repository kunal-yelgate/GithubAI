from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import auth
from app.routes import github
from app.routes import ai
from app.config import FRONTEND_URL


app = FastAPI(
    title="GitHub AI Repo Analyzer"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        origin.strip()
        for origin in (FRONTEND_URL or "http://localhost:5173").split(",")
        if origin.strip()
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router)
app.include_router(github.router)
app.include_router(ai.router)

@app.get("/")
async def root():

    return {
        "message": "GitHub AI Repo Analyzer API is running"
    }
