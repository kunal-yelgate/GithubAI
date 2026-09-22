import asyncio
import unittest
from unittest.mock import AsyncMock, patch

from app.ai.llm import AIProviderError, ask_llm


class AskLLMProviderFallbackTests(unittest.TestCase):
    def test_falls_back_to_mistral_on_groq_auth_failure(self):
        async def run_test():
            with patch("app.ai.llm._request_provider", new_callable=AsyncMock) as mock_request, \
                 patch("app.ai.llm.MISTRAL_API_KEY", "mistral-key"), \
                 patch("app.ai.llm.GROQ_API_KEY", "gsk_test_key"), \
                 patch("app.ai.llm.AI_PROVIDER", "groq"):
                mock_request.side_effect = [
                    AIProviderError("groq request failed: unauthorized"),
                    {"answer": "ok", "provider": "mistral", "model": "mistral-small-latest"},
                ]

                result = await ask_llm([{"role": "user", "content": "hello"}])

                self.assertEqual(result["provider"], "mistral")
                self.assertEqual(mock_request.call_count, 2)

        asyncio.run(run_test())


if __name__ == "__main__":
    unittest.main()
