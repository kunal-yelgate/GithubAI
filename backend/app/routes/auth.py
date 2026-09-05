from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse

from app.services.github_oauth import (
    get_github_login_url,
    exchange_code_for_token
)

from app.services.github_api import (
    get_github_user,
    get_user_repositories
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.get("/github")
async def github_login():

    github_url = get_github_login_url()

    return RedirectResponse(github_url)


@router.get("/github/callback")
async def github_callback(code: str):

    # 1. Exchange OAuth code for access token
    token_data = await exchange_code_for_token(code)

    if "access_token" not in token_data:

        raise HTTPException(
            status_code=400,
            detail="Failed to authenticate with GitHub"
        )

    access_token = token_data["access_token"]

    # 2. Get GitHub user
    user = await get_github_user(access_token)

    # 3. Get repositories
    repositories = await get_user_repositories(access_token)

    return {
        "message": "GitHub authentication successful",
        "user": user,
        "repositories": repositories
    }