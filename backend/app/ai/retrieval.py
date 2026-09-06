import json
import re

from app.ai.chunker import chunk_file
from app.ai.embeddings import cosine_similarity, embed_texts
from app.database.repositories import get_code_chunks, replace_code_chunks
from app.services.github_api import get_repository, get_repository_file
from app.services.analysis_service import analyze_repository_cached


def _terms(value: str):
    return set(re.findall(r"[a-zA-Z_][a-zA-Z0-9_]{2,}", value.lower()))


async def index_repository(access_token: str, owner: str, repo: str):
    analysis, cached = await analyze_repository_cached(access_token, owner, repo)
    repository = await get_repository(access_token, owner, repo)
    full_name = repository["full_name"]
    source_version = repository.get("pushed_at") or repository.get("updated_at")
    paths = analysis.get("important_files", {}).get("important_files", [])
    chunks = []

    for path in paths:
        try:
            content = await get_repository_file(access_token, owner, repo, path)
        except Exception:
            continue
        chunks.extend(chunk_file(path, content))

    embeddings = await embed_texts([chunk["content"] for chunk in chunks])
    if embeddings:
        for chunk, embedding in zip(chunks, embeddings):
            chunk["embedding"] = embedding

    replace_code_chunks(full_name, source_version, chunks)
    return {"repository": full_name, "chunks": len(chunks), "embedded": bool(embeddings), "analysis_cached": cached}


async def retrieve_chunks(access_token: str, owner: str, repo: str, question: str, limit: int = 3):
    full_name = f"{owner}/{repo}"
    chunks = get_code_chunks(full_name)
    if not chunks:
        await index_repository(access_token, owner, repo)
        chunks = get_code_chunks(full_name)

    query_embedding = await embed_texts([question])
    question_terms = _terms(question)
    scored = []
    for chunk in chunks:
        score = 0.0
        if query_embedding and chunk.get("embedding"):
            score = cosine_similarity(query_embedding[0], json.loads(chunk["embedding"]))
        else:
            content_terms = _terms(chunk["file_path"] + " " + chunk["content"])
            score = len(question_terms & content_terms) / max(len(question_terms), 1)
        scored.append((score, chunk))

    return [chunk for _, chunk in sorted(scored, key=lambda item: item[0], reverse=True)[:limit]]