import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

DATABASE_URL = (os.getenv("DATABASE_URL") or os.getenv("NEON_DATABASE") or "").strip()

GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
GITHUB_REDIRECT_URI = os.getenv("GITHUB_REDIRECT_URI")

FRONTEND_URL = os.getenv("FRONTEND_URL")

GROK_API_KEY = (os.getenv("GROK_API_KEY") or "").strip().strip('"').strip("'")
GROQ_API_KEY = (os.getenv("GROQ_API_KEY") or "").strip().strip('"').strip("'")
MISTRAL_API_KEY = (os.getenv("MISTRAL_API_KEY") or "").strip().strip('"').strip("'")
AI_PROVIDER = os.getenv("AI_PROVIDER")
if not AI_PROVIDER:
	AI_PROVIDER = "groq" if GROQ_API_KEY else "grok"
AI_PROVIDER = AI_PROVIDER.lower().strip()
AI_MODEL = os.getenv("AI_MODEL")