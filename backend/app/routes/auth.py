from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse

from app.services.github_oauth import (
    get_github_login_url,
    exchange_code_for_token
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.get("/github")
async def github_login():

    github_url = get_github_login_url()

    return RedirectResponse(github_url)


@router.get("/github/callback")
async def github_callback(code: str):

    token_data = await exchange_code_for_token(code)

    if "access_token" not in token_data:
        raise HTTPException(
            status_code=400,
            detail="Failed to authenticate with GitHub"
        )

    access_token = token_data["access_token"]

    return {
        "message": "GitHub authentication successful",
        "access_token": access_token
    }