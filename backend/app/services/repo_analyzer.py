import asyncio

from app.services.github_api import (
    get_repository,
    get_repository_languages,
    get_repository_commits,
    get_repository_tree,
    get_repository_file,
    get_repository_readme
)

from app.analyzers.language_analyzer import (
    analyze_languages
)

from app.analyzers.structure_analyzer import (
    analyze_structure
)

from app.analyzers.commit_analyzer import (
    analyze_commits
)

from app.analyzers.activity_analyzer import analyze_activity
from app.analyzers.technology_analyzer import (
    analyze_package_json,
    analyze_requirements,
    detect_technologies
)
from app.analyzers.readme_analyzer import analyze_readme
from app.analyzers.file_detector import detect_important_files
from app.analyzers.source_analyzer import analyze_source_files
from app.analyzers.architecture_analyzer import analyze_architecture


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

    try:
        language_data = await get_repository_languages(
            access_token,
            owner,
            repo
        )
        language_analysis = analyze_languages(language_data)
    except Exception:
        language_analysis = {
            "primary_language": None,
            "languages": {},
            "total_bytes": 0
        }

    # Commits
    try:
        commits = await get_repository_commits(
            access_token,
            owner,
            repo,
            max_pages=10
        )
    except Exception:
        commits = []
    
    commit_analysis = analyze_commits(
        commits
    )

    activity_analysis = analyze_activity(commits)

    tree = await get_repository_tree(
        access_token,
        owner,
        repo,
        repository.get("default_branch") or "main"
    )

    structure_analysis = analyze_structure(tree)
    files = structure_analysis["files"]
    technologies = detect_technologies(files)
    dependencies = {}

    important_file_analysis = detect_important_files(files)
    selected_files = important_file_analysis["important_files"]
    source_contents = {}

    async def fetch_source(path: str):
        try:
            return path, await get_repository_file(access_token, owner, repo, path)
        except Exception:
            return path, None

    fetched_files = await asyncio.gather(*(fetch_source(path) for path in selected_files))

    for path, content in fetched_files:
        if content is None:
            continue

        if path.endswith("package.json"):
            try:
                package_analysis = analyze_package_json(content)
                dependencies[path] = package_analysis["dependencies"]
                technologies.extend(package_analysis["technologies"])
            except Exception:
                pass
        elif path.endswith("requirements.txt"):
            try:
                requirements_analysis = analyze_requirements(content)
                dependencies[path] = requirements_analysis["dependencies"]
                technologies.extend(requirements_analysis["technologies"])
            except Exception:
                pass

        if path.rsplit(".", 1)[-1].lower() in {"py", "js", "jsx", "ts", "tsx"}:
            source_contents[path] = content

    try:
        readme_content = await get_repository_readme(
            access_token,
            owner,
            repo
        )
    except Exception:
        readme_content = None

    technologies = sorted(set(technologies))
    source_analysis = analyze_source_files(source_contents)

    return {
        "repository": {
            "name": repository.get("name"),
            "full_name": repository.get("full_name"),
            "description": repository.get("description"),
            "stars": repository.get("stargazers_count", 0),
            "forks": repository.get("forks_count", 0),
            "open_issues": repository.get("open_issues_count", 0),
            "default_branch": repository.get("default_branch") or "main"
        },

        "languages": language_analysis,

        "structure": structure_analysis,

        "technologies": technologies,
        "dependencies": dependencies,
        "commits": commit_analysis,
        "activity": activity_analysis,
        "readme": analyze_readme(readme_content),
        "important_files": important_file_analysis,
        "source_analysis": source_analysis,
        "architecture": analyze_architecture(files, technologies, source_analysis)
    }


