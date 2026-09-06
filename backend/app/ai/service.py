from app.ai.context import build_messages, profile_context, repository_context
from app.ai.llm import ask_llm
from app.ai.retrieval import retrieve_chunks
from app.services.analysis_service import analyze_repository_cached
from app.services.github_api import get_user_repositories


async def answer_question(
    access_token: str,
    question: str,
    owner: str | None = None,
    repo: str | None = None,
    provider: str | None = None
):
    if not question.strip():
        raise ValueError("Question cannot be empty")

    if bool(owner) != bool(repo):
        raise ValueError("Both owner and repo are required for repository questions")

    if owner and repo:
        analysis, cached = await analyze_repository_cached(access_token, owner, repo)
        chunks = await retrieve_chunks(access_token, owner, repo, question)
        context = repository_context(analysis, chunks)
        context["cache"] = {"used": cached}
    else:
        repositories = await get_user_repositories(access_token)
        context = profile_context(repositories)

    result = await ask_llm(build_messages(question, context), provider)
    return {**result, "scope": f"{owner}/{repo}" if owner else "profile"}