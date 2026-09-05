from app.services.github_api import (
    get_repository,
    get_repository_languages,
    get_repository_commits
)

from app.analyzers.language_analyzer import (
    analyze_languages
)


async def analyze_repository(
    access_token: str,
    owner: str,
    repo: str
):

    # Repository metadata
    repository = await get_repository(
        access_token,
        owner,
        repo
    )

    # Languages
    language_data = await get_repository_languages(
        access_token,
        owner,
        repo
    )

    language_analysis = analyze_languages(
        language_data
    )

    # Commits
    commits = await get_repository_commits(
        access_token,
        owner,
        repo
    )

    return {
        "repository": {
            "name": repository["name"],
            "full_name": repository["full_name"],
            "description": repository["description"],
            "stars": repository["stargazers_count"],
            "forks": repository["forks_count"],
            "open_issues": repository["open_issues_count"],
            "default_branch": repository["default_branch"]
        },

        "languages": language_analysis,

        "commits": {
            "fetched": len(commits)
        }
    }