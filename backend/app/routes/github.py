from fastapi import APIRouter, Cookie, HTTPException

from app.session import read_session
from app.services.github_api import (
    get_github_user,
    get_user_repositories
)
from app.services.repo_analyzer import analyze_repository


router = APIRouter(
    prefix="/github",
    tags=["GitHub"]
)


def get_access_token(session: str | None) -> str:

    if not session:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated"
        )

    try:
        session_data = read_session(session)
        return session_data["access_token"]
    except Exception as error:
        raise HTTPException(
            status_code=401,
            detail="Invalid session"
        ) from error


@router.get("/me")
async def current_user(
    session: str | None = Cookie(default=None)
):

    access_token = get_access_token(session)
    return await get_github_user(access_token)


@router.get("/repositories")
async def user_repositories(
    session: str | None = Cookie(default=None)
):

    access_token = get_access_token(session)
    return await get_user_repositories(access_token)


@router.get("/repositories/{owner}/{repo}/analysis")
async def analyze_repo(
    owner: str,
    repo: str,
    session: str | None = Cookie(default=None)
):

    access_token = get_access_token(session)

    result = await analyze_repository(
        access_token,
        owner,
        repo
    )

    return result