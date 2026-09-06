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
        repo,
        max_pages=10
    )
    
    commit_analysis = analyze_commits(
        commits
    )

    activity_analysis = analyze_activity(commits)

    tree = await get_repository_tree(
        access_token,
        owner,
        repo,
        repository["default_branch"]
    )

    structure_analysis = analyze_structure(tree)
    files = structure_analysis["files"]
    technologies = detect_technologies(files)
    dependencies = {}

    important_file_analysis = detect_important_files(files)
    selected_files = important_file_analysis["important_files"]
    source_contents = {}

    for path in selected_files:
        try:
            content = await get_repository_file(
                access_token,
                owner,
                repo,
                path
            )
        except Exception:
            continue

        if path.endswith("package.json"):
            package_analysis = analyze_package_json(content)
            dependencies[path] = package_analysis["dependencies"]
            technologies.extend(package_analysis["technologies"])
        elif path.endswith("requirements.txt"):
            requirements_analysis = analyze_requirements(content)
            dependencies[path] = requirements_analysis["dependencies"]
            technologies.extend(requirements_analysis["technologies"])

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
            "name": repository["name"],
            "full_name": repository["full_name"],
            "description": repository["description"],
            "stars": repository["stargazers_count"],
            "forks": repository["forks_count"],
            "open_issues": repository["open_issues_count"],
            "default_branch": repository["default_branch"]
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
        "architecture": analyze_architecture(files, technologies)
    }


