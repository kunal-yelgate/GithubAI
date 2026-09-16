from fastapi.testclient import TestClient

from app.ai.context import SYSTEM_PROMPT
from app.analyzers.commit_analyzer import analyze_commits
from app.main import app


client = TestClient(app)


def test_github_callback_requires_code(monkeypatch):
    monkeypatch.setattr(
        "app.routes.auth.exchange_code_for_token",
        lambda code: {"access_token": "fake-token"},
    )
    monkeypatch.setattr(
        "app.routes.auth.create_session",
        lambda access_token: "signed-session",
    )

    response = client.get("/auth/github/callback")

    assert response.status_code == 400
    assert response.json()["detail"] == "Missing GitHub OAuth code"


def test_analyze_commits_includes_history_and_authors():
    commits = [
        {
            "sha": "abc123",
            "author": {"login": "alice"},
            "commit": {
                "message": "Fix login flow\n\nDetails",
                "author": {"name": "Alice", "date": "2024-01-02T00:00:00Z"}
            },
            "html_url": "https://example.com/commit/abc123"
        },
        {
            "sha": "def456",
            "author": {"login": "bob"},
            "commit": {
                "message": "Add dashboard stats",
                "author": {"name": "Bob", "date": "2024-01-01T00:00:00Z"}
            },
            "html_url": "https://example.com/commit/def456"
        }
    ]

    analysis = analyze_commits(commits)

    assert analysis["total_analyzed"] == 2
    assert analysis["history"][0]["author"] == "alice"
    assert analysis["history"][0]["message"] == "Fix login flow"
    assert analysis["history"][1]["author"] == "bob"


def test_system_prompt_requires_repository_evidence():
    assert "Repository descriptions are weak evidence" in SYSTEM_PROMPT
    assert "source file analysis" in SYSTEM_PROMPT
    assert "retrieved code snippets" in SYSTEM_PROMPT
