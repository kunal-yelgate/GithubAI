import httpx
import base64

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

async def get_repository_languages(
    access_token: str,
    owner: str,
    repo: str
):

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    async with httpx.AsyncClient() as client:

        response = await client.get(
            f"{GITHUB_API_URL}/repos/{owner}/{repo}/languages",
            headers=headers
        )

        response.raise_for_status()

        return response.json()

async def get_repository(
    access_token: str,
    owner: str,
    repo: str
):

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    async with httpx.AsyncClient() as client:

        response = await client.get(
            f"{GITHUB_API_URL}/repos/{owner}/{repo}",
            headers=headers
        )

        response.raise_for_status()

        return response.json()

async def get_repository_commits(
    access_token: str,
    owner: str,
    repo: str
):

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    params = {
        "per_page": 100
    }

    async with httpx.AsyncClient() as client:

        response = await client.get(
            f"{GITHUB_API_URL}/repos/{owner}/{repo}/commits",
            headers=headers,
            params=params
        )

        response.raise_for_status()

        return response.json()

async def get_repository_tree(
    access_token: str,
    owner: str,
    repo: str,
    branch: str = "main"
):

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    async with httpx.AsyncClient() as client:

        response = await client.get(
            f"{GITHUB_API_URL}/repos/"
            f"{owner}/{repo}/git/trees/{branch}",
            headers=headers,
            params={
                "recursive": "1"
            }
        )

        response.raise_for_status()

        return response.json()

async def get_repository_file(
    access_token: str,
    owner: str,
    repo: str,
    path: str
):

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    async with httpx.AsyncClient() as client:

        response = await client.get(
            f"{GITHUB_API_URL}/repos/"
            f"{owner}/{repo}/contents/{path}",
            headers=headers
        )

        response.raise_for_status()

        data = response.json()

        content = base64.b64decode(
            data["content"]
        ).decode("utf-8")

        return content