from fastapi import APIRouter, Cookie, HTTPException

from app.session import read_session
from app.services.github_api import (
    get_github_user,
    get_user_repositories
)

router = APIRouter(
    prefix="/github",
    tags=["GitHub"]
)


@router.get("/me")
async def get_me(session: str | None = Cookie(default=None)):

    if not session:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated"
        )

    try:
        session_data = read_session(session)

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid session"
        )

    access_token = session_data["access_token"]

    user = await get_github_user(access_token)

    return user


@router.get("/repositories")
async def get_repositories(
    session: str | None = Cookie(default=None)
):

    if not session:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated"
        )

    try:
        session_data = read_session(session)

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid session"
        )

    access_token = session_data["access_token"]

    repositories = await get_user_repositories(
        access_token
    )

    return repositories