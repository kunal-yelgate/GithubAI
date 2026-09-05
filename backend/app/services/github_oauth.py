import httpx

from app.config import (
    GITHUB_CLIENT_ID,
    GITHUB_CLIENT_SECRET,
    GITHUB_REDIRECT_URI
)

GITHUB_AUTHORIZE_URL = "https://github.com/login/oauth/authorize"
GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"

def get_github_login_url():

    return (
        f"{GITHUB_AUTHORIZE_URL}"
        f"?client_id={GITHUB_CLIENT_ID}"
        f"&redirect_uri={GITHUB_REDIRECT_URI}"
        f"&scope=read:user%20repo"
    )


async def exchange_code_for_token(code: str):

    data = {
        "client_id": GITHUB_CLIENT_ID,
        "client_secret": GITHUB_CLIENT_SECRET,
        "code": code,
        "redirect_uri": GITHUB_REDIRECT_URI
    }

    headers = {
        "Accept": "application/json"
    }

    async with httpx.AsyncClient() as client:

        response = await client.post(
            GITHUB_TOKEN_URL,
            data=data,
            headers=headers
        )

        response.raise_for_status()

        return response.json()