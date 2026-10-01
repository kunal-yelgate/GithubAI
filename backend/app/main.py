from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import auth
from app.routes import github
from app.routes import ai
from app.config import FRONTEND_URL


app = FastAPI(
    title="GitHub AI Repo Analyzer"
)


configured_origins = [
    origin.strip().rstrip("/")
    for origin in (FRONTEND_URL or "").split(",")
    if origin.strip()
]

default_origins = [
    "https://githubai-anly.vercel.app",
    "http://localhost:5173",
    "http://localhost:3000",
    "http://127.0.0.1:5173",
]

allowed_origins = list(dict.fromkeys(configured_origins + default_origins))

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_origin_regex=r"https://.*\.vercel\.app",
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
