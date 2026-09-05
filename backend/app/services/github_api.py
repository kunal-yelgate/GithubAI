import httpx

GITHUB_API_URL = "https://api.github.com"


async def get_github_user(access_token: str):

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    async with httpx.AsyncClient() as client:

        response = await client.get(
            f"{GITHUB_API_URL}/user",
            headers=headers
        )

        response.raise_for_status()

        return response.json()


async def get_user_repositories(access_token: str):

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    params = {
        "per_page": 100,
        "sort": "updated"
    }

    async with httpx.AsyncClient() as client:

        response = await client.get(
            f"{GITHUB_API_URL}/user/repos",
            headers=headers,
            params=params
        )

        response.raise_for_status()

        return response.json()