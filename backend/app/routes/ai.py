from fastapi import APIRouter, Cookie, HTTPException
from pydantic import BaseModel, Field

from app.ai.llm import AIProviderError
from app.ai.service import answer_question
from app.ai.retrieval import index_repository
from app.routes.github import get_access_token


router = APIRouter(prefix="/ai", tags=["AI"])


class ChatRequest(BaseModel):
    question: str = Field(min_length=1, max_length=4000)
    owner: str | None = None
    repo: str | None = None
    provider: str | None = None


@router.post("/chat")
async def chat(request: ChatRequest, session: str | None = Cookie(default=None)):
    access_token = get_access_token(session)
    try:
        return await answer_question(
            access_token,
            request.question,
            request.owner,
            request.repo,
            request.provider
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    except AIProviderError as error:
        raise HTTPException(status_code=502, detail=str(error)) from error


@router.post("/index/{owner}/{repo}")
async def index_repo(owner: str, repo: str, session: str | None = Cookie(default=None)):
    access_token = get_access_token(session)
    try:
        return await index_repository(access_token, owner, repo)
    except Exception as error:
        raise HTTPException(status_code=502, detail=f"Repository indexing failed: {error}") from error