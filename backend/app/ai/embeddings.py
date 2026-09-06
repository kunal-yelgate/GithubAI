import math

import httpx

from app.config import MISTRAL_API_KEY


async def embed_texts(texts: list[str]):
    if not MISTRAL_API_KEY or MISTRAL_API_KEY.startswith("replace-after"):
        return None

    async with httpx.AsyncClient(timeout=90) as client:
        response = await client.post(
            "https://api.mistral.ai/v1/embeddings",
            headers={"Authorization": f"Bearer {MISTRAL_API_KEY}"},
            json={"model": "mistral-embed", "input": texts}
        )
    response.raise_for_status()
    return [item["embedding"] for item in response.json()["data"]]


def cosine_similarity(left: list[float], right: list[float]):
    numerator = sum(a * b for a, b in zip(left, right))
    left_norm = math.sqrt(sum(value * value for value in left))
    right_norm = math.sqrt(sum(value * value for value in right))
    if not left_norm or not right_norm:
        return 0.0
    return numerator / (left_norm * right_norm)