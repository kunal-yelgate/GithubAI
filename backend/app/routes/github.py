from fastapi import APIRouter, Cookie, HTTPException

from app.session import read_session
from app.services.repo_analyzer import analyze_repository


router = APIRouter(
    prefix="/github",
    tags=["GitHub"]
)


@router.get("/repositories/{owner}/{repo}/analysis")
async def analyze_repo(
    owner: str,
    repo: str,
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

    result = await analyze_repository(
        access_token,
        owner,
        repo
    )

    return result