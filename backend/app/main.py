from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import auth

app = FastAPI(
    title="GitHub AI Repo Analyzer"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router)

@app.get("/")
async def root():

    return {
        "message": "GitHub AI Repo Analyzer API is running"
    }