from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_root_endpoint_html_for_browser():
    response = client.get("/", headers={"accept": "text/html"})
    assert response.status_code == 200
    assert "PocketSmart AI" in response.text
    assert "<html" in response.text.lower()


def test_register_and_login():
    suffix = uuid4().hex[:8]
    email = f"demo_{suffix}@example.com"
    username = f"demo_user_{suffix}"

    register_response = client.post(
        "/auth/register",
        json={
            "email": email,
            "username": username,
            "password": "secret123",
        },
    )
    assert register_response.status_code == 200

    login_response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": "secret123",
        },
    )
    assert login_response.status_code == 200
    assert "access_token" in login_response.json()


def test_planner_endpoint():
    response = client.post(
        "/planner",
        json={
            "destination": "Paris",
            "budget": 350,
            "days": 3,
            "interests": ["food", "history"],
            "travelers": 2,
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["destination"] == "Paris"
    assert payload["title"]
    assert len(payload["itinerary"]) >= 1
