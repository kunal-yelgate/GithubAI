from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from app.session import create_session

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


@router.post("/logout")
async def logout():
    response = JSONResponse({"signed_out": True})
    response.delete_cookie(
        key="session",
        httponly=True,
        secure=False,
        samesite="lax"
    )
    return response


@router.get("/github/callback")
async def github_callback(
    code: str | None = None,
    error: str | None = None,
    error_description: str | None = None,
):
    if error:
        raise HTTPException(
            status_code=400,
            detail=(error_description or error or "GitHub authentication failed")
        )

    if not code:
        raise HTTPException(
            status_code=400,
            detail="Missing GitHub OAuth code"
        )

    token_data = await exchange_code_for_token(code)

    if "access_token" not in token_data:
        raise HTTPException(
            status_code=400,
            detail="GitHub authentication failed"
        )

    access_token = token_data["access_token"]

    session = create_session(access_token)

    response = RedirectResponse(
        url="http://localhost:5173/dashboard"
    )

    response.set_cookie(
        key="session",
        value=session,
        httponly=True,
        secure=False,  # True in production HTTPS
        samesite="lax",
        path="/"
    )

    return response