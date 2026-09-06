import json

from app.database.repositories import list_cached_analyses


SYSTEM_PROMPT = """You are GitHub Atlas, a precise repository intelligence assistant.
Answer only from the supplied GitHub context. Never invent files, metrics, technologies, or code.
When citing evidence, use repository-relative file paths in backticks. Explain uncertainty when context is incomplete.
For statistics and profile questions, calculate from the supplied structured data.
For code questions, distinguish static-analysis findings from direct source excerpts.
Keep answers useful and concise, with short headings or bullets when appropriate."""

MAX_CONTEXT_CHARS = 18000


def _compact_analysis(analysis: dict):
    return {
        "repository": analysis.get("repository", {}),
        "languages": analysis.get("languages", {}),
        "technologies": analysis.get("technologies", []),
        "dependencies": analysis.get("dependencies", {}),
        "commits": analysis.get("commits", {}),
        "activity": analysis.get("activity", {}),
        "readme": analysis.get("readme", {}),
        "important_files": analysis.get("important_files", {}),
        "source_analysis": analysis.get("source_analysis", []),
        "architecture": analysis.get("architecture", {})
    }


def repository_context(analysis: dict, chunks: list[dict]):
    return {
        "analysis": _compact_analysis(analysis),
        "retrieved_code_chunks": [
            {
                "file": chunk["file_path"],
                "language": chunk["language"],
                "chunk_index": chunk["chunk_index"],
                "content": chunk["content"][:2400]
            }
            for chunk in chunks[:4]
        ]
    }


def profile_context(repositories: list[dict]):
    cached_by_name = {
        analysis.get("repository", {}).get("full_name"): analysis
        for analysis in list_cached_analyses()
    }
    repository_summary = [
        {
            "full_name": repository.get("full_name"),
            "description": repository.get("description"),
            "language": repository.get("language"),
            "stars": repository.get("stargazers_count", 0),
            "forks": repository.get("forks_count", 0)
        }
        for repository in repositories
    ]
    return {
        "repositories": repository_summary,
        "cached_analyses": [
            _compact_analysis(cached_by_name[repo["full_name"]])
            for repo in repositories
            if repo["full_name"] in cached_by_name
        ]
    }


def build_messages(question: str, context: dict):
    context_text = json.dumps(context, separators=(",", ":"), default=str)
    if len(context_text) > MAX_CONTEXT_CHARS:
        context_text = context_text[:MAX_CONTEXT_CHARS] + "\n[context truncated]"

    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": (
                f"GitHub context:\n{context_text}\n\n"
                f"User question: {question}"
            )
        }
    ]