from fastapi.testclient import TestClient

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
