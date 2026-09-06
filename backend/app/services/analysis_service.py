from app.database.repositories import get_cached_analysis, save_analysis
from app.services.github_api import get_repository
from app.services.repo_analyzer import analyze_repository


async def analyze_repository_cached(access_token: str, owner: str, repo: str):
    repository = await get_repository(access_token, owner, repo)
    full_name = repository["full_name"]
    source_version = repository.get("pushed_at") or repository.get("updated_at")

    cached = get_cached_analysis(full_name, source_version)
    if cached:
        return cached, True

    result = await analyze_repository(access_token, owner, repo)
    save_analysis(full_name, source_version, result)
    return result, False


def build_profile(analyses: list[dict]):
    language_counts = {}
    technology_counts = {}
    total_commits = 0

    for analysis in analyses:
        for language in analysis.get("languages", {}).get("languages", {}):
            language_counts[language] = language_counts.get(language, 0) + 1
        for technology in analysis.get("technologies", []):
            technology_counts[technology] = technology_counts.get(technology, 0) + 1
        total_commits += analysis.get("commits", {}).get("total_analyzed", 0)

    most_active = max(
        analyses,
        key=lambda item: item.get("commits", {}).get("total_analyzed", 0),
        default=None
    )
    most_starred = max(
        analyses,
        key=lambda item: item.get("repository", {}).get("stars", 0),
        default=None
    )

    return {
        "total_repositories": len(analyses),
        "total_commits_analyzed": total_commits,
        "languages": dict(sorted(language_counts.items(), key=lambda item: (-item[1], item[0]))),
        "technologies": dict(sorted(technology_counts.items(), key=lambda item: (-item[1], item[0]))),
        "most_active_repository": most_active["repository"]["full_name"] if most_active else None,
        "most_starred_repository": most_starred["repository"]["full_name"] if most_starred else None
    }