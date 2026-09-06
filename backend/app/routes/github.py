from fastapi import APIRouter, Cookie, HTTPException

from app.session import read_session
from app.services.github_api import (
    get_github_user,
    get_user_repositories
)
from app.services.analysis_service import (
    analyze_repository_cached,
    build_profile
)


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

    result, cached = await analyze_repository_cached(
        access_token,
        owner,
        repo
    )

    return {**result, "cached": cached}


@router.post("/analyze-all")
async def analyze_all_repositories(
    session: str | None = Cookie(default=None)
):
    access_token = get_access_token(session)
    repositories = await get_user_repositories(access_token)
    analyses = []
    failures = []

    for repository in repositories:
        try:
            analysis, _ = await analyze_repository_cached(
                access_token,
                repository["owner"]["login"],
                repository["name"]
            )
            analyses.append(analysis)
        except Exception as error:
            failures.append({
                "full_name": repository.get("full_name"),
                "error": str(error)
            })

    return {
        "profile": build_profile(analyses),
        "analyses": analyses,
        "failures": failures
    }