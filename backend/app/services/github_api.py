import asyncio
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


async def get_user_contribution_counts(access_token: str, username: str):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    async with httpx.AsyncClient() as client:
        pull_requests_response, issues_response = await asyncio.gather(
            client.get(
                f"{GITHUB_API_URL}/search/issues",
                headers=headers,
                params={"q": f"author:{username} type:pr", "per_page": 1}
            ),
            client.get(
                f"{GITHUB_API_URL}/search/issues",
                headers=headers,
                params={"q": f"author:{username} type:issue", "per_page": 1}
            )
        )

    pull_requests_response.raise_for_status()
    issues_response.raise_for_status()
    return {
        "pull_requests": pull_requests_response.json().get("total_count", 0),
        "issues": issues_response.json().get("total_count", 0)
    }

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
    repo: str,
    max_pages: int = 10
):

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    commits = []

    async with httpx.AsyncClient() as client:
        for page in range(1, max_pages + 1):
            response = await client.get(
                f"{GITHUB_API_URL}/repos/{owner}/{repo}/commits",
                headers=headers,
                params={"per_page": 100, "page": page}
            )

            response.raise_for_status()
            page_commits = response.json()
            commits.extend(page_commits)

            if len(page_commits) < 100:
                break

    return commits

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


async def get_repository_readme(
    access_token: str,
    owner: str,
    repo: str
):
    return await get_repository_file(
        access_token,
        owner,
        repo,
        "README.md"
    )