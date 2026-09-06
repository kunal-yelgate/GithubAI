import httpx

from app.config import (
    AI_MODEL,
    AI_PROVIDER,
    GROK_API_KEY,
    GROQ_API_KEY,
    MISTRAL_API_KEY
)


PROVIDERS = {
    "grok": {
        "url": "https://api.x.ai/v1/chat/completions",
        "default_model": "grok-3-mini",
        "key": GROK_API_KEY
    },
    "groq": {
        "url": "https://api.groq.com/openai/v1/chat/completions",
        "default_model": "openai/gpt-oss-120b",
        "key": GROQ_API_KEY or (GROK_API_KEY if GROK_API_KEY.startswith("gsk_") else "")
    },
    "mistral": {
        "url": "https://api.mistral.ai/v1/chat/completions",
        "default_model": "mistral-small-latest",
        "key": MISTRAL_API_KEY
    }
}


class AIProviderError(RuntimeError):
    pass


async def _request_provider(messages: list[dict], provider_name: str):
    settings = PROVIDERS.get(provider_name)
    if not settings:
        raise AIProviderError(f"Unsupported AI provider: {provider_name}")
    if not settings["key"] or settings["key"].startswith("replace-after"):
        raise AIProviderError(f"{provider_name} API key is not configured")

    payload = {
        "model": AI_MODEL or settings["default_model"],
        "messages": messages,
        "temperature": 0.2,
        "max_tokens": 1200
    }
    headers = {
        "Authorization": f"Bearer {settings['key']}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient(timeout=90) as client:
        response = await client.post(settings["url"], headers=headers, json=payload)

    if response.is_error:
        detail = response.text[:500]
        raise AIProviderError(f"{provider_name} request failed: {detail}")

    data = response.json()
    try:
        answer = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as error:
        raise AIProviderError("AI provider returned an unexpected response") from error

    return {"answer": answer, "provider": provider_name, "model": payload["model"]}


async def ask_llm(messages: list[dict], provider: str | None = None):
    provider_name = (provider or AI_PROVIDER).lower()
    if provider_name == "grok" and GROK_API_KEY.startswith("gsk_"):
        provider_name = "groq"
    try:
        return await _request_provider(messages, provider_name)
    except AIProviderError as error:
        error_text = str(error).lower()
        if provider is None and provider_name == "groq" and "context_length" in error_text:
            return await _request_provider(messages, "mistral")
        raise